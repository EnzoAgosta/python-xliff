import unittest
from xliff.objects import ContextGroup, Context
from xliff.constants import CONTEXT_TYPE, PURPOSE


class TestContextGroup(unittest.TestCase):
  def test_init_with_explicit_values(self) -> None:
    contexts = [
      Context(value="Hello", context_type="sourcefile"),
      Context(value="World", context_type="linenumber"),
    ]
    group = ContextGroup(
      name="main", purpose="location", contexts=contexts, crc="beef1234"
    )

    self.assertEqual(group.name, "main")
    self.assertEqual(group.purpose, PURPOSE.LOCATION)
    self.assertEqual(len(group.contexts), 2)
    self.assertEqual(group.contexts[1].value, "World")

  def test_to_element_round_trip(self) -> None:
    original = ContextGroup(
      name="meta",
      purpose=PURPOSE.LOCATION,
      contexts=[
        Context(value="A", context_type="sourcefile"),
        Context(value="B", context_type="linenumber"),
      ],
    )
    element = original.to_element()
    parsed = ContextGroup(source_element=element)
    self.assertEqual(parsed.name, "meta")
    self.assertEqual(parsed.purpose, PURPOSE.LOCATION)
    self.assertEqual(len(parsed.contexts), 2)
    self.assertEqual(parsed.contexts[0].context_type, CONTEXT_TYPE.SOURCEFILE)

  def test_validate_success(self) -> None:
    group = ContextGroup(
      contexts=[
        Context(value="test", context_type="sourcefile"),
        Context(value="data", context_type="linenumber"),
      ]
    )
    self.assertTrue(group.validate())
    self.assertTrue(group.validate(recurse=True))


class TestContextGroupMalformedData(unittest.TestCase):
  def test_invalid_purpose_raises(self) -> None:
    with self.assertRaises(ValueError):
      ContextGroup(purpose="not-a-purpose").validate()

  def test_invalid_context_in_recurse(self) -> None:
    good = Context(value="Good", context_type="sourcefile")
    bad = Context(value="Bad", context_type="sourcefile")
    bad.crc = 12345  # type: ignore

    group = ContextGroup(contexts=[good, bad])
    with self.assertRaises(TypeError):
      group.validate(recurse=True)

  def test_non_string_crc_in_validate(self) -> None:
    group = ContextGroup(contexts=[], crc=1234)  # type: ignore
    with self.assertRaises(TypeError):
      group.validate()
