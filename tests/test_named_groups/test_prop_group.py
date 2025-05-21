import unittest
from typing import MutableSequence
from xliff.errors import ValidationError
from xliff.named_groups import PropGroup, Prop
from lxml.etree import Element


class TestPropGroup(unittest.TestCase):
  def setUp(self) -> None:
    # Create sample props for testing
    self.sample_prop1 = Prop(value="test1", prop_type="type1")
    self.sample_prop2 = Prop(value="test2", prop_type="type2")
    self.sample_props = [self.sample_prop1, self.sample_prop2]

  def test_init_with_explicit_values(self) -> None:
    prop_group = PropGroup(name="test_group", props=self.sample_props)
    self.assertEqual(prop_group.name, "test_group")
    self.assertEqual(len(prop_group.props), 2)
    self.assertIsInstance(prop_group.props, MutableSequence)

  def test_init_with_source_element(self) -> None:
    # Create a source element with required attributes
    source = Element("prop-group", {"name": "source_group"})
    # Add some prop children
    prop1 = Element("prop", {"prop-type": "type1"})
    prop1.text = "test1"
    prop2 = Element("prop", {"prop-type": "type2"})
    prop2.text = "test2"
    source.append(prop1)
    source.append(prop2)

    prop_group = PropGroup(source_element=source)
    self.assertEqual(prop_group.name, "source_group")
    self.assertEqual(len(prop_group.props), 2)
    self.assertEqual(prop_group.props[0].value, "test1")
    self.assertEqual(prop_group.props[1].value, "test2")

  def test_init_with_empty_props(self) -> None:
    prop_group = PropGroup(name="empty_group", props=[])
    self.assertEqual(len(prop_group.props), 0)

  def test_validate_success(self) -> None:
    prop_group = PropGroup(name="valid_group", props=self.sample_props)
    # Should not raise any exceptions
    prop_group.validate()

  def test_validate_missing_name(self) -> None:
    with self.assertWarns(UserWarning):
      prop_group = PropGroup(props=self.sample_props)  # type: ignore
    with self.assertRaises(ValidationError):
      prop_group.validate()

  def test_validate_invalid_props(self) -> None:
    # Create a prop group with an invalid prop
    with self.assertWarns(UserWarning):
      invalid_prop = Prop(value="test", prop_type=None)  # type: ignore
    prop_group = PropGroup(name="test_group", props=[invalid_prop])
    with self.assertRaises(ValidationError):
      prop_group.validate(recurse=True)

  def test_to_element_round_trip(self) -> None:
    original = PropGroup(name="test_group", props=self.sample_props)
    # Convert to element and back
    element = original.to_element()
    restored = PropGroup(source_element=element)

    # Verify properties are preserved
    self.assertEqual(restored.name, original.name)
    self.assertEqual(len(restored.props), len(original.props))
    for orig_prop, restored_prop in zip(original.props, restored.props):
      self.assertEqual(restored_prop.value, orig_prop.value)
      self.assertEqual(restored_prop.prop_type, orig_prop.prop_type)

  def test_props_modification(self) -> None:
    prop_group = PropGroup(name="test_group", props=[])
    # Test adding props
    prop_group.props.append(self.sample_prop1)
    self.assertEqual(len(prop_group.props), 1)

    # Test removing props
    prop_group.props.remove(self.sample_prop1)
    self.assertEqual(len(prop_group.props), 0)

  def test_to_element_attributes(self) -> None:
    prop_group = PropGroup(name="test_group", props=self.sample_props)
    element = prop_group.to_element()
    self.assertEqual(element.tag, "prop-group")
    self.assertEqual(element.get("name"), "test_group")
    self.assertEqual(len(element), 2)  # Should have 2 child elements
