"""
Utilities for extracting data from Opal applications
"""
import csv
import datetime
import functools
import logging

import os
import tempfile
import zipfile

from search.extract_rules import ExtractRule

from django.template import Context, loader


def chunk_list(some_list, amount):
    for i in range(0, len(some_list), amount):
        yield some_list[i:i + amount]


def get_datadictionary_context(user, in_page=False):
    serializers = list(ExtractRule.list_rules(user))
    return dict(
        data_dictionary=dict(
            serializers=serializers,
            chunked_columns=chunk_list(serializers, 5),
            in_page=in_page
        )
    )


def write_data_dictionary(file_name, user):
    t = loader.get_template("search/data_dictionary_download.html")
    ctx = Context(get_datadictionary_context(user))
    rendered = t.render(ctx)
    with open(file_name, "w") as f:
        f.write(rendered)


def generate_flat_csv_extract(root_dir, episodes, user, field_dict):
    """ Generate a a single csv file and the data dictionary

        The field_dict should be {api_name: [field_names]}

        The csv file will only contain the files mentioned in the field_dict
    """
    file_names = []
    data_dict_file_name = "data_dictionary.html"
    full_file_name = os.path.join(root_dir, data_dict_file_name)
    write_data_dictionary(full_file_name, user)
    file_names.append((full_file_name, data_dict_file_name,))
    csv_file_name = "extract.csv"
    full_file_name = os.path.join(root_dir, csv_file_name)
    file_names.append((full_file_name, csv_file_name,))
    renderers = []
    rules = []
    for model_api_name, model_fields in field_dict.items():
        rules.append(ExtractRule.get_rule(
            model_api_name, user
        ))

    rules = ExtractRule.sort_rules(rules)
    for rule in rules:
        renderer_cls = rule.get_renderer()

        renderers.append(renderer_cls(
            rule,
            episodes,
            user,
            chosen_fields_names=field_dict[rule.get_api_name()]
        ))

    with open(full_file_name, 'w') as csv_file:
        writer = csv.writer(csv_file)
        headers = []
        for renderer in renderers:
            headers.extend(renderer.get_flat_headers())
        writer.writerow(headers)

        for episode in episodes:
            row = []
            for renderer in renderers:
                row.extend(renderer.get_flat_row(episode))
            writer.writerow(row)
    return file_names


def write_multi_csv_to_file(file_name, renderer):
    logging.info("writing for {}".format(
        renderer.serializer.get_display_name())
    )

    with open(file_name, "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(renderer.get_headers())
        for row in renderer.get_rows():
            writer.writerow([i for i in row])

    logging.info("finished writing for {}".format(
        renderer.serializer.get_display_name())
    )


def generate_multi_csv_extract(root_dir, episodes, user):
    """ Generate the files and return a tuple of absolute_file_name, file_name
    """
    file_names = []

    file_name = "data_dictionary.html"
    full_file_name = os.path.join(root_dir, file_name)
    write_data_dictionary(full_file_name, user)
    file_names.append((full_file_name, file_name,))

    full_file_name = os.path.join(root_dir, file_name)

    for serializer in ExtractRule.list_rules(user):
        file_name = "{}.csv".format(serializer.get_api_name())
        full_file_name = os.path.join(root_dir, file_name)
        renderer_cls = serializer.get_renderer()
        renderer = renderer_cls(serializer, episodes, user)
        if renderer.exists():
            write_multi_csv_to_file(full_file_name, renderer)
            file_names.append((full_file_name, file_name,))

    return file_names


def get_description_with_fields(episodes, user, description, fields):
    field_description = []
    for serializer_name, field_names in fields.items():
        serializer = ExtractRule.get_rule(serializer_name, user)
        if serializer:
            serializer_fields = serializer.get_fields()
            serializer_fields = [
                i for i in serializer_fields if i.field_name in field_names
            ]
            field_names = [i.get_display_name() for i in serializer_fields]
            field_description.append(
                "{} - {}".format(
                    serializer.get_display_name(),
                    ", ".join(sorted(field_names))
                )
            )
    if field_description:
        return "{description} \nExtracting:\n{fields}".format(
            description=description,
            fields="\n".join(field_description)
        )

    # ie where someone is trying to extract a subrecord
    # that is not extractable
    return description


def write_description(episodes, user, description, root_dir, fields=None):
    query_file_name = "query.txt"
    full_query_file_name = os.path.join(root_dir, query_file_name)
    if fields:
        description = get_description_with_fields(
            episodes, user, description, fields
        )

    with open(full_query_file_name, "w") as f:
        f.write(description)

    return full_query_file_name, query_file_name


def zip_archive(episodes, description, user, fields=None):
    """
    Given an iterable of EPISODES, the DESCRIPTION of this set of episodes,
    and the USER for which we are extracting, create a zip archive suitable
    for download with all of these episodes as CSVs.
    """
    target_dir = tempfile.mkdtemp()
    target = os.path.join(target_dir, 'extract.zip')

    with zipfile.ZipFile(target, mode='w') as z:
        zipfolder = '{0}.{1}'.format(user.username, datetime.date.today())
        root_dir = os.path.join(target_dir, zipfolder)
        os.mkdir(root_dir)
        zip_relative_file_path = functools.partial(os.path.join, zipfolder)
        full_query_file_name, query_file_name = write_description(
            episodes, user, description, root_dir, fields=fields
        )
        z.write(full_query_file_name, zip_relative_file_path(query_file_name))

        if fields:
            file_names = generate_flat_csv_extract(
                root_dir, episodes, user, fields
            )
        else:
            file_names = generate_multi_csv_extract(root_dir, episodes, user)

        for full_file_name, file_name in file_names:
            z.write(
                full_file_name,
                zip_relative_file_path(file_name)
            )

    return target


def async_extract(user, extract_query):
    """
    Given the user and the criteria, let's run an async extract.
    """
    from search import tasks
    return tasks.extract.delay(user, extract_query).id
