from mock import patch
from opal.core.test import OpalTestCase
from opal.tests.models import Colour, HoundOwner
from elcid import models
from search import subrecord_discoverable
from search.exceptions import SearchException


class FieldWrapper(subrecord_discoverable.SubrecordFieldWrapper):
    field_name = "name"


class SomeSubrecordWithModel(
    subrecord_discoverable.SubrecordFieldWrapper
):
    model = Colour
    field_name = "name"


class SomeSubrecordWithModelOverrides(
    subrecord_discoverable.SubrecordFieldWrapper
):
    model = Colour
    field_name = "name"
    display_name = "interesting"
    enum = ["Sarah", "Michelle"]
    lookup_list = "first_names"
    type_display_name = "something"
    type = "string"


class SubrecordFieldWrapperWithoutUnderlyingField(
    subrecord_discoverable.SubrecordFieldWrapper
):
    display_name = "interesting"
    enum = ["Sarah", "Michelle"]
    lookup_list = "first_names"
    type_display_name = "something"
    type = "string"


class SubrecordFieldWrapperTestCase(OpalTestCase):
    def test_sets_model_if_not_already_set(self):
        # without passing it in, we're None
        field_wrapper_1 = SubrecordFieldWrapperWithoutUnderlyingField(
            self.user, field_name="name"
        )
        self.assertIsNone(field_wrapper_1.model)
        self.assertEqual(field_wrapper_1.field_name, "name")

        # with passing it in, we're set
        field_wrapper_2 = SubrecordFieldWrapperWithoutUnderlyingField(
            self.user, Colour, "name"
        )
        self.assertEqual(
            field_wrapper_2.model, Colour
        )
        self.assertEqual(
            field_wrapper_2.field_name, "name"
        )

    def test_overwrites_model_if_already_set(self):
        field_wrapper_1 = SomeSubrecordWithModel(
            self.user
        )
        self.assertEqual(
            field_wrapper_1.model, Colour
        )
        self.assertEqual(
            field_wrapper_1.field_name, "name"
        )

        field_wrapper_2 = SomeSubrecordWithModel(
            self.user, models.PresentingComplaint, "duration"
        )
        self.assertEqual(
            field_wrapper_2.model, models.PresentingComplaint
        )
        self.assertEqual(
            field_wrapper_2.field_name, "duration"
        )

    def test_throw_error_if_no_field_name(self):
        class SomeSubrecordWithNoFieldName(
            subrecord_discoverable.SubrecordFieldWrapper
        ):
            pass
        with self.assertRaises(NotImplementedError):
            SomeSubrecordWithNoFieldName(self.user)

    def test_sets_user(self):
        field_wrapper_1 = SomeSubrecordWithModel(
            self.user
        )
        self.assertEqual(
            field_wrapper_1.user, self.user
        )

    def test_field_fk_or_ft(self):
        field_wrapper = subrecord_discoverable.SubrecordFieldWrapper(
            self.user, HoundOwner, "dog"
        )
        self.assertEqual(
            field_wrapper.field,
            HoundOwner.dog
        )

    def test_field_other(self):
        field_wrapper = subrecord_discoverable.SubrecordFieldWrapper(
            self.user, Colour, "name"
        )
        # extract the lazy object
        field_wrapper.field.name
        self.assertEqual(
            field_wrapper.field,
            Colour._meta.get_field("name")
        )

    def test_to_dict_with_model(self):
        field_wrapper = subrecord_discoverable.SubrecordFieldWrapper(
            self.user, Colour, "name"
        )
        expected = {
            'model': 'Colour',
            'lookup_list': None,
            'default': None,
            'description': None,
            'enum': None,
            'name': 'name',
            'display_name': u'Name',
            'type': 'string',
            'icon': 'fa fa-comments'
        }
        self.assertEqual(field_wrapper.to_dict(), expected)

    def test_to_dict_with_model_overrides(self):
        field_wrapper = SomeSubrecordWithModelOverrides(self.user)
        expected = {
            'model': 'Colour',
            'lookup_list': 'first_names',
            'default': None,
            'description': None,
            'enum': ['Sarah', 'Michelle'],
            'name': 'name',
            'display_name': 'interesting',
            'type': 'string',
            'icon': 'fa fa-comments'
        }
        self.assertEqual(field_wrapper.to_dict(), expected)

    def test_to_dict_without_model(self):
        field_wrapper = SubrecordFieldWrapperWithoutUnderlyingField(
            self.user, field_name="name"
        )
        expected = {
            'lookup_list': 'first_names',
            'enum': ['Sarah', 'Michelle'],
            'name': 'name',
            'type': 'string',
            'display_name': 'interesting',
        }
        self.assertEqual(field_wrapper.to_dict(), expected)


class DiscoverableMock(object):
    @classmethod
    def list(cls):
        return []

    @classmethod
    def list_rules(cls, user):
        return []


class ColourOverride(
    subrecord_discoverable.SubrecordDiscoverableMixin,
    DiscoverableMock
):
    model = Colour

    @classmethod
    def get_slug(cls):
        return Colour.get_api_name()


class SubrecordDiscoverableMixinTestCase(OpalTestCase):
    def test_stores_model(self):
        a = subrecord_discoverable.SubrecordDiscoverableMixin(
            self.user, model=Colour
        )
        self.assertEqual(a.model, Colour)

    def test_stores_user(self):
        a = subrecord_discoverable.SubrecordDiscoverableMixin(
            self.user
        )
        self.assertEqual(a.user, self.user)

    @patch("search.subrecord_discoverable.subrecords.subrecords")
    def test_list_without_model(self, subrecords):
        class SubrecordDiscoverableSubclass(
            subrecord_discoverable.SubrecordDiscoverableMixin
        ):
            slug = "something"
            subrecords.return_value = []

            def __init__(self, *args, **kwargs):
                pass

            @classmethod
            def get_slug(kls):
                return kls.slug

        class SubrecordDiscoverable(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            pass

        with patch.object(DiscoverableMock, "list_rules") as l:
            l.return_value = (
                i for i in [SubrecordDiscoverableSubclass(self.user)]
            )
            found_rules = list(DiscoverableMock.list_rules(self.user))
            self.assertEqual(
                len(found_rules), 1
            )
            self.assertEqual(
                found_rules[0].slug,
                "something"
            )

            self.assertTrue(
                isinstance(found_rules[0], SubrecordDiscoverableSubclass),
            )

    @patch("search.subrecord_discoverable.subrecords.subrecords")
    def test_list_override_model(self, subrecords):
        subrecords.return_value = [Colour]

        class SubrecordDiscoverableSubclass(
            subrecord_discoverable.SubrecordDiscoverableMixin,
        ):
            slug = Colour.get_api_name()

            def __init__(self, *args, **kwargs):
                pass

            @classmethod
            def get_slug(kls):
                return kls.slug

        class SubrecordDiscoverable(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            pass

        with patch.object(DiscoverableMock, "list_rules") as l:
            l.return_value = [SubrecordDiscoverableSubclass]

            self.assertEqual(
                len(list(SubrecordDiscoverable.list_rules(self.user))), 1
            )
            api_name = next(
                SubrecordDiscoverable.list_rules(self.user)
            ).get_api_name()
            self.assertEqual(
                api_name,
                Colour.get_api_name()
            )

            self.assertTrue(
                next(SubrecordDiscoverable.list_rules(self.user)),
                SubrecordDiscoverableSubclass
            )

    @patch("search.subrecord_discoverable.subrecords.subrecords")
    def test_list_model(self, subrecords):
        subrecords.return_value = [Colour]

        class SubrecordDiscoverable(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            @classmethod
            def get_slug(cls):
                return None

        self.assertEqual(
            len(list(SubrecordDiscoverable.list_rules(self.user))), 1
        )
        self.assertEqual(
            next(SubrecordDiscoverable.list_rules(self.user)).get_api_name(),
            Colour.get_api_name()
        )

        self.assertEqual(
            next(SubrecordDiscoverable.list_rules(self.user)).__class__,
            SubrecordDiscoverable
        )

    @patch("search.subrecord_discoverable.subrecords.subrecords")
    def test_list_exclude(self, subrecords):
        subrecords.return_value = [Colour]

        class ColourOverride(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            model = Colour
            exclude = True

            @classmethod
            def get_slug(cls):
                return Colour.get_api_name()

        class SubrecordDiscoverable(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            @classmethod
            def get_slug(cls):
                return None

        with patch.object(DiscoverableMock, "list") as l:
            l.return_value = [ColourOverride]
            self.assertEqual(
                len(list(SubrecordDiscoverable.list_rules(self.user))), 0
            )

    def test_cast_field_name_to_attribute(self):
        with patch.object(ColourOverride, "attribute_cls") as attr_cls:
            sub_discoverable = ColourOverride(self.user)
            result = sub_discoverable.cast_field_name_to_attribute("x")
            attr_cls.assert_called_once_with(
                self.user, Colour, "x"
            )
            self.assertEqual(result, attr_cls())

    def test_cast_field_name_to_attribute_error(self):
        with self.assertRaises(NotImplementedError):
            sub_discoverable = ColourOverride(self.user)
            sub_discoverable.cast_field_name_to_attribute("x")

    def test_get_model_fields_error(self):
        with self.assertRaises(NotImplementedError):
            sub_discoverable = ColourOverride(self.user)
            sub_discoverable.get_model_fields()

    def test_get_fields_error(self):
        with self.assertRaises(NotImplementedError):
            sub_discoverable = ColourOverride(self.user)
            sub_discoverable.get_model_fields()

    def test_get_model_fields_with_field(self):
        class NameOverride(subrecord_discoverable.SubrecordFieldWrapper):
            field_name = "name"

        class ColourOverride(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            model = Colour
            fields = [NameOverride]

        colour_override = ColourOverride(self.user)
        with patch.object(colour_override, "get_model_fields") as gmf:
            gmf.return_value = []

        fields = list(colour_override.get_fields())
        self.assertEqual(len(fields), 1)
        self.assertTrue(isinstance(fields[0], NameOverride))

    def test_get_model_fields_with_field_string(self):
        class HoundOwnerOverride(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            model = HoundOwner
            fields = ["name"]
            attribute_cls = FieldWrapper
        hound_owner_override = HoundOwnerOverride(self.user)
        with patch.object(hound_owner_override, "get_model_fields") as gmf:
            gmf.return_value = ["name", "dog"]

        fields = list(hound_owner_override.get_fields())
        self.assertEqual(len(list(fields)), 1)
        self.assertTrue(isinstance(fields[0], FieldWrapper))
        self.assertTrue(fields[0].field_name, "name")

    def test_get_field(self):
        with patch.object(ColourOverride, "get_fields") as gf:
            gf.return_value = [SomeSubrecordWithModel(self.user)]
            field = ColourOverride(self.user).get_field("name")
            self.assertTrue(isinstance(field, SomeSubrecordWithModel))

    def test_get_field_exception(self):
        with patch.object(ColourOverride, "get_fields") as gf:
            with self.assertRaises(SearchException):
                gf.return_value = [SomeSubrecordWithModel(self.user)]
                ColourOverride(self.user).get_field("onions")

    def test_get_display_name_self_display_name(self):
        class SomethingElse(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            display_name = "Onion"
        self.assertEqual(
            SomethingElse(self.user).get_display_name(), "Onion"
        )

    def test_get_display_name_from_model(self):
        class ColourOverride(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            model = Colour
        self.assertEqual(
            ColourOverride(self.user).get_display_name(),
            "Colour"
        )

    def test_get_display_raises_error(self):
        class SomethingElse(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            pass

        with self.assertRaises(NotImplementedError):
            SomethingElse(self.user).get_display_name(),

    def test_local_display_name_overrides_model(self):
        class ColourOverride(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            display_name = "Onion"
            model = Colour
        self.assertEqual(
            ColourOverride(self.user).get_display_name(), "Onion"
        )

    def test_get_description(self):
        class ColourOverride(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            model = Colour
            description = "A hazy shade of winter"
        self.assertEqual(
            ColourOverride(self.user).get_description(),
            "A hazy shade of winter"
        )

    def test_get_api_name_from_slug(self):
        class SomethingElse(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            slug = "tree"

        self.assertEqual(
            SomethingElse(self.user).get_api_name(),
            "tree"
        )

    def test_get_api_name_from_model(self):
        self.assertEqual(
            ColourOverride(self.user).get_api_name(),
            Colour.get_api_name()
        )

    def test_get_api_name_error(self):
        class SomethingElse(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            pass
        with self.assertRaises(NotImplementedError):
            SomethingElse(self.user).get_api_name()

    def test_get_icon(self):
        class ColourOverride(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            model = Colour
            icon = "some_icon"

        self.assertEqual(
            ColourOverride(self.user).get_icon(),
            "some_icon"
        )

    def get_icon_model(self):
        sub = subrecord_discoverable.SubrecordDiscoverableMixin(
            model=models.ContactDetails
        )
        self.assertEqual(
            sub.get_icon(), 'fa fa-phone'
        )

    def test_get_schemas(self):
        class FieldWrapper(subrecord_discoverable.SubrecordFieldWrapper):
            pass

        class SubrecordDiscoverable(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            attribute_cls = FieldWrapper

            @classmethod
            def get_slug(cls):
                return None

            def get_model_fields(self):
                return self.model._get_fieldnames_to_serialize()

        colour_override = ColourOverride(self.user)
        with patch.object(colour_override, "get_schema") as gs:
            with patch.object(SubrecordDiscoverable, "list_rules") as l:
                l.return_value = [colour_override]
                gs.return_value = {"display_name": "schema"}

                self.assertEqual(
                    SubrecordDiscoverable.get_schemas(self.user),
                    [{"display_name": "schema"}]
                )

    def test_get_schema(self):
        class HoundOwnerOverride(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            model = HoundOwner
            attribute_cls = FieldWrapper
            description = "something"

        hound_owner_override = HoundOwnerOverride(self.user)
        with patch.object(hound_owner_override, "get_model_fields") as gmf:
            # fields should be resorted into alphabetical order
            gmf.return_value = ["name", "dog"]
            schema = hound_owner_override.get_schema()
            self.assertEqual(
                schema["fields"][0]["display_name"], "Hound",
            )

            self.assertEqual(
                schema["fields"][1]["display_name"], "Name",
            )

        self.assertEqual(
            schema["name"], "hound_owner"
        )
        self.assertEqual(
            schema["display_name"], "Hound Owner"
        )
        self.assertEqual(
            schema["description"], "something"
        )

    def test_get_schema_fields_override_order(self):
        class HoundOwnerOverride(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            model = HoundOwner
            attribute_cls = FieldWrapper
            description = "something"
            fields = ["name", "dog"]

        hound_owner_override = HoundOwnerOverride(self.user)
        with patch.object(hound_owner_override, "get_model_fields") as gmf:
            # fields should be resorted into alphabetical order
            gmf.return_value = ["name", "dog"]
            schema = hound_owner_override.get_schema()
            self.assertEqual(
                schema["fields"][0]["display_name"], "Name",
            )

            self.assertEqual(
                schema["fields"][1]["display_name"], "Hound",
            )

    def test_sort_fields(self):
        class HoundOwnerOverride(
            subrecord_discoverable.SubrecordDiscoverableMixin,
            DiscoverableMock
        ):
            model = HoundOwner
            attribute_cls = FieldWrapper
            description = "something"

        fields = [
            FieldWrapper(
                self.user,
                model=HoundOwner,
                field_name="name"
            ),
            FieldWrapper(
                self.user,
                model=HoundOwner,
                field_name="dog"
            )
        ]
        hound_owner_override = HoundOwnerOverride(self.user)
        self.assertEqual(
            hound_owner_override.sort_fields(fields),
            [fields[1], fields[0]]
        )
