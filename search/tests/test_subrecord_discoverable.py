from opal.core.test import OpalTestCase
from search import subrecord_discoverable
from elcid import models
from opal.tests.models import Colour, HoundOwner


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
    description = "very interesting"
    enum = ["Sarah", "Michelle"]
    lookup_list = "first_names"
    type_display_name = "something"
    type = "string"


class SubrecordFieldWrapperWithoutUnderlyingField(
    subrecord_discoverable.SubrecordFieldWrapper
):
    display_name = "interesting"
    description = "very interesting"
    enum = ["Sarah", "Michelle"]
    lookup_list = "first_names"
    type_display_name = "something"
    type = "string"


class SubrecordFieldWrapperTestCase(OpalTestCase):
    def test_sets_model_if_not_already_set(self):
        # without passing it in, we're None
        field_wrapper_1 = SubrecordFieldWrapperWithoutUnderlyingField(
            self.user
        )
        self.assertIsNone(field_wrapper_1.model)
        self.assertIsNone(field_wrapper_1.field_name)

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
            'enum': None,
            'description': None,
            'name': 'name',
            'display_name': u'Name',
            'type': 'string',
            'type_display_name': 'Text Field'
        }
        self.assertEqual(field_wrapper.to_dict(), expected)

    def test_to_dict_with_model_overrides(self):
        field_wrapper = SomeSubrecordWithModelOverrides(self.user)
        expected = {
            'model': 'Colour',
            'lookup_list': 'first_names',
            'default': None,
            'enum': ['Sarah', 'Michelle'],
            'description': 'very interesting',
            'name': 'name',
            'display_name': 'interesting',
            'type': 'string',
            'type_display_name': 'something'
        }
        self.assertEqual(field_wrapper.to_dict(), expected)

    def test_to_dict_without_model(self):
        field_wrapper = SubrecordFieldWrapperWithoutUnderlyingField(
            self.user, field_name="name"
        )
        expected = {
            'lookup_list': 'first_names',
            'enum': ['Sarah', 'Michelle'],
            'description': 'very interesting',
            'name': 'name',
            'display_name': 'interesting',
            'type': 'string',
            'type_display_name': 'something'
        }
        self.assertEqual(field_wrapper.to_dict(), expected)
