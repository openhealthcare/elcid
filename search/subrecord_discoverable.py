from django.utils.encoding import force_str
from django.db import models as djangomodels

from opal.core import subrecords
from opal.core import fields


from search.exceptions import SearchException


class SubrecordFieldWrapper(object):
    def __init__(self, model, field_name):
        self.model = model
        self.field_name = field_name

    @property
    def field(self):
        if isinstance(
            getattr(self.model, self.field_name), fields.ForeignKeyOrFreeText
        ):
            return getattr(self.model, self.field_name)
        return self.model._meta.get_field(self.field_name)

    def get_slug(self):
        return self.field_name

    def get_display_name(self):
        return self.model._get_field_title(self.field_name)

    def get_description(self):
        field = self.field
        description = self.description

        if description:
            return description

        enum = self.model.get_field_enum(self.field_name)

        if enum:
            return "One of {}".format(", ".join([force_str(e) for e in enum]))

        related_fields = (
            djangomodels.ForeignKey, djangomodels.ManyToManyField,
        )

        if isinstance(field, fields.ForeignKeyOrFreeText):
            t = "Text"

        if isinstance(field, related_fields):
            if isinstance(field, djangomodels.ForeignKey):
                t = "One of the {}"
            else:
                t = "Some of the {}"
            related = field.rel.to
            return t.format(related._meta.verbose_name_plural.title())


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
    description = ""
    model = None

    # set this to True if you want it to be excluded
    # from the list, for example if the model should not be
    # searchable
    exclude = False

    def __init__(self, model=None):
        if model is not None:
            self.model = model

    @classmethod
    def get(cls, slug):
        for field in cls.list():
            if field.get_api_name() == slug:
                return field

    @classmethod
    def list(klass):
        declared_classes = super(SubrecordDiscoverableMixin, klass).list()
        declared_slugs = set()

        for declared_class in declared_classes:
            declared_slugs.add(declared_class.get_slug())
            if declared_class.exclude:
                continue
            else:
                yield declared_class()

        for subrecord in subrecords.subrecords():
            if subrecord.get_api_name() not in declared_slugs:
                yield klass(subrecord)

    def cast_field_name_to_attribute(self, str):
        return self.attribute_cls(self.model, str)

    def get_model_fields(self):
        raise NotImplementedError(
            "which fields do you want to get off the model"
        )

    def get_fields(self):
        if not hasattr(self, "fields"):
            if not self.model:
                raise SearchException(
                    "Fields must be declared on {}".format(
                        self
                    )
                )

        fields = self.fields
        if fields is None:
            fields = self.get_model_fields()

        for field in fields:
            if isinstance(field, (str, unicode,)):
                if not hasattr(self.model, field):
                    raise SearchException(
                        "Unable to find field {} for {}".format(
                            field, self.get_display_name()
                        )
                    )
                yield self.cast_field_name_to_attribute(field)
            else:
                yield field()

    def get_field(self, field_name):
        for i in self.get_fields():
            if i.get_slug() == field_name:
                return i
        raise SearchException("Unable to find field {} for {}".format(
            field_name, self.get_display_name()
        ))

    def get_display_name(self):
        if self.display_name:
            return self.display_name
        if self.model:
            return self.model.get_display_name()
        raise NotImplementedError("please implement a display name on {}")

    def get_api_name(self):
        if self.slug:
            return self.slug
        if self.model:
            return self.model.get_api_name()
        raise NotImplementedError("please implement a slug name on {}")

    def get_icon(self):
        if self.model:
            return self.model.get_icon()
