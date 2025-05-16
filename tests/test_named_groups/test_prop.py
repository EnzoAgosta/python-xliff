import unittest
from xliff.errors import ValidationError
from xliff.objects import Prop


class TestProp(unittest.TestCase):
  def test_init_with_explicit_values(self) -> None:
    prop = Prop(value="Some value", prop_type="important-data", lang="en-US")
    self.assertEqual(prop.value, "Some value")
    self.assertEqual(prop.prop_type, "important-data")
    self.assertEqual(prop.lang, "en-US")

  def test_to_element_round_trip(self) -> None:
    original = Prop(value="Metadata", prop_type="metadata", lang="fr-FR")
    element = original.to_element()
    parsed = Prop(source_element=element)
    self.assertEqual(parsed.value, "Metadata")
    self.assertEqual(parsed.prop_type, "metadata")
    self.assertEqual(parsed.lang, "fr-FR")

  def test_validate_success(self) -> None:
    prop = Prop(value="Test", prop_type="test-type")
    prop.validate()


class TestPropMalformedData(unittest.TestCase):
  def test_missing_value_warns(self) -> None:
    with self.assertWarns(UserWarning):
      Prop(prop_type="metadata")  # type: ignore

  def test_missing_prop_type_warns(self) -> None:
    with self.assertWarns(UserWarning):
      Prop(value="test")  # type: ignore

  def test_invalid_type_in_validate(self) -> None:
    prop = Prop(value="ok", prop_type="test")
    prop.lang = 1234  # type: ignore
    with self.assertRaises(ValidationError):
      prop.validate()
