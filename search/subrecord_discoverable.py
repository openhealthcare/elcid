from functools import wraps
import itertools
from opal import models
from opal.core import subrecords
from opal.core import fields
from opal.utils import camelcase_to_underscore
from search.exceptions import SearchException
from django.db import models as djangomodels


def get_locally_or_defer(field_name):
    def under_wrap(some_fun):
        """
        If we have a field, for example 'description'
        check to see if that is set object before calling
        through
        """
        @wraps(some_fun)
        def func_wrapper(self):
            locally = getattr(self, field_name)
            if locally is not None:
                return locally
            return some_fun(self)
        return func_wrapper
    return under_wrap


def is_boolean_field(some_field):
    return isinstance(
        some_field, (djangomodels.BooleanField, djangomodels.NullBooleanField,)
    )


def is_text_type_field(some_field):
    return isinstance(
        some_field, (djangomodels.TextField, djangomodels.CharField,)
    )


def is_date_field(some_field):
    return isinstance(
        some_field, (djangomodels.DateField, djangomodels.DateTimeField,)
    )


def is_date_time_field(some_field):
    return isinstance(
        some_field, djangomodels.DateTimeField
    )


def is_time_field(some_field):
    return isinstance(
        some_field, djangomodels.TimeField
    )


def is_many_to_many_field(some_field):
    return isinstance(
        some_field, djangomodels.ManyToManyField
    )


def is_foreign_key_or_free_text_field(some_field):
    return isinstance(
        some_field, fields.ForeignKeyOrFreeText
    )


def is_foreign_key_field(some_field):
    return isinstance(
        some_field, djangomodels.ForeignKey
    )


def get_team_display_name_to_slug():
    result = {}
    tagging_schema = models.Tagging.build_field_schema()
    for schema in tagging_schema:
        result[schema["title"]] = schema["name"]

    tag_slugs = set(
        models.Tagging.objects.values_list("value", flat=True).distinct()
    )

    result_slugs = set(result.values())

    for tag_slug in tag_slugs:
        if tag_slug not in result_slugs:
            title = camelcase_to_underscore(tag_slug).replace("_", " ").title()
            result[title] = tag_slug

    return result


class SubrecordFieldWrapper(object):
    model = None
    field_name = None
    description = None
    display_name = None
    enum = None
    icon = None
    # the lookup list associated
    lookup_list = None
    # the display name of the slug
    type_display_name = None
    # the type of field as a slug
    type = None

    def __init__(self, user, model=None, field_name=None):
        if model is not None:
            self.model = model
        if field_name is not None:
            self.field_name = field_name
        self.user = user
        if not self.field_name:
            raise NotImplementedError(
                "A subrecord field wrapper requires a field name"
            )

    @property
    def field(self):
        if isinstance(
            getattr(self.model, self.field_name, None),
            fields.ForeignKeyOrFreeText
        ):
            return getattr(self.model, self.field_name)
        if self.model:
            return self.model._meta.get_field(self.field_name)

    def to_dict(self):
        if self.model:
            schema = self.model.build_schema_for_field_name(self.field_name)
            schema["display_name"] = schema.pop("title")
        else:
            schema = {}

        fields = [
            "enum",
            "name",
            "description",
            "display_name",
            "lookup_list",
            "icon",
        ]
        for i in fields:
            attr = getattr(self, "get_{}".format(i))()
            if attr:
                schema[i] = attr

        field_type = self.get_field_type()
        if field_type:
            schema["type"] = field_type
        return schema

    @get_locally_or_defer("enum")
    def get_enum(self):
        if self.model:
            return self.model.get_field_enum(self.field_name)

    def get_name(self):
        return self.field_name

    def get_field_type(self):
        return self.type

    @get_locally_or_defer("display_name")
    def get_display_name(self):
        return self.model._get_field_title(self.field_name)

    @get_locally_or_defer("icon")
    def get_icon(self):
        if self.model and hasattr(self.model, "get_icon"):
            return self.model.get_icon()

    @get_locally_or_defer("type_display_name")
    def get_type_display_name(self):
        return self.model.get_human_readable_type(
            self.field_name
        )

    @get_locally_or_defer("lookup_list")
    def get_lookup_list(self):
        if self.model:
            return self.model.get_lookup_list_api_name(self.field_name)

    def get_lookup_list_display_name(self):
        ll = self.get_lookup_list()
        if ll:
            return ll.replace("_", " ").title()

    @get_locally_or_defer("description")
    def get_description(self):
        if self.model:
            field = self.model._get_field(self.field_name)
            description = getattr(field, 'help_text', "")
            if description:
                return description

    def __str__(self):
        return "{}: {} - {}".format(
            self.__class__, self.get_display_name(), self.get_name()
        )

    def __unicode__(self):
        return self.__str__()


class SubrecordDiscoverableMixin(object):
    """
        This is a derivation of a discoverable
        except, if it cannot find what you
        are looking for it looks for a subrecord
        with that api name.

        Its different from a discoverable as it
        does not return the class.

        Instead it initialises itself and then
        returns itself. Initialising with a subrecord
        if found.

        It also assumes that you will want
        to wrap the attributes of the subrecord
        in some form of wrapper.
        for that it uses whatever is set as
        the attribute_cls.
    """
    attribute_cls = None
    description = None
    model = None
    fields = None
    display_name = None
    include_in_schema = True
    slug = None

    # defines the order used by list, otherwise gets added to the end
    # alphabetically
    order = None

    # set this to True if you want it to be excluded
    # from the list, for example if the model should not be
    # searchable
    exclude = False

    def __init__(self, user, model=None):
        self.user = user

        if model is not None:
            self.model = model

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return "{}: {}".format(self.__class__, self.get_display_name())

    @classmethod
    def get_rule(cls, slug, user):
        for field in cls.list_rules(user):
            if field.get_api_name() == slug:
                return field

    @classmethod
    def sort_rules(klass, rules):
        ordered = []
        alphabetical = []

        for i in rules:
            if i.order:
                ordered.append(i)
            else:
                alphabetical.append(i)

        ordered = sorted(ordered, key=lambda x: x.order)
        alphabetical = sorted(alphabetical, key=lambda x: x.get_display_name())
        return itertools.chain(ordered, alphabetical)

    @classmethod
    def list_rules(klass, user):
        declared_classes = super(SubrecordDiscoverableMixin, klass).list()
        declared_slugs = set()
        result = []

        for declared_class in declared_classes:
            declared_slugs.add(declared_class.get_slug())
            declared_instance = declared_class(user)
            if declared_instance.exclude:
                continue
            else:
                result.append(declared_instance)

        for subrecord in subrecords.subrecords():
            if subrecord.get_api_name() not in declared_slugs:
                result.append(klass(user, subrecord))
        return klass.sort_rules(result)

    def cast_field_name_to_attribute(self, str):
        if not self.attribute_cls:
            raise NotImplementedError(
                "Please set an attribute class on {}".format(self)
            )

        return self.attribute_cls(self.user, self.model, str)

    def get_model_fields(self):
        raise NotImplementedError(
            "which fields do you want to get off the model"
        )

    def sort_fields(self, fields):
        """
        If the fields attribute is declared, use the order specified.
        However if we are pulling out model fields, we should
        order them alphabetically.
        """
        return sorted(fields, key=lambda x: x.get_display_name())

    def get_fields(self):
        """
        Get all fields,
        if they are declared as a `fields` attribute use that in the order
        they are declared.

        otherwise use the model fields, sorted by `sort_model_fields`
        (defaults to alphabetical)
        """
        class_attr = "fields"
        if not hasattr(self, class_attr):
            if not self.model:
                raise SearchException(
                    "{} must be declared on {}".format(
                        class_attr, self
                    )
                )

        fields = self.fields
        if fields is None:
            fields = self.get_model_fields()

        result = []

        for field in fields:
            if isinstance(field, (str, unicode,)):
                # you can override individual fields by declaring at an attr
                # field_{} field_name
                local_field_name = "field_{}".format(field)
                if hasattr(self, local_field_name):
                    result.append(getattr(self, local_field_name)(self.user))
                elif hasattr(self.model, field):
                    result.append(self.cast_field_name_to_attribute(field))
                else:
                    raise SearchException(
                        "Unable to find field {} for {}".format(
                            field, self.get_display_name()
                        )
                    )
            else:
                result.append(field(self.user))

        # if fields are declared explicitly then we use the
        # ordering defined
        if self.fields:
            return result
        else:
            return self.sort_fields(result)

    def get_field(self, field_name):
        for i in self.get_fields():
            if i.get_name() == field_name:
                return i
        raise SearchException("Unable to find field {} for {}".format(
            field_name, self.get_display_name()
        ))

    @get_locally_or_defer("display_name")
    def get_display_name(self):
        if self.model:
            return self.model.get_display_name()
        raise NotImplementedError("please implement a display name on {}")

    def get_description(self):
        return self.description

    def get_api_name(self):
        if self.slug:
            return self.slug
        if self.model:
            return self.model.get_api_name()
        raise NotImplementedError("please implement a slug name on {}")

    @get_locally_or_defer("icon")
    def get_icon(self):
        if self.model:
            return self.model.get_icon()

    @classmethod
    def get_schemas(cls, user):
        return [i.get_schema() for i in cls.list_rules(user)]

    def get_fields_for_schema(self):
        """ Whether this field should appear in the schema
        """
        return self.get_fields()

    def get_schema(self):
        fields = self.get_fields_for_schema()
        fields = [i.to_dict() for i in self.get_fields_for_schema()]

        return dict(
            name=self.get_api_name(),
            display_name=self.get_display_name(),
            fields=fields,
            description=self.get_description()
        )
