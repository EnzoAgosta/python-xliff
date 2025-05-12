import unittest
from xliff.objects import Context
from xliff.constants import CONTEXT_TYPE


class TestContext(unittest.TestCase):
  def test_init_with_explicit_values(self) -> None:
    ctx = Context(
      value="FileName.java",
      context_type="sourcefile",
      match_mandatory=True,
      crc="1234ABCD",
    )
    self.assertEqual(ctx.value, "FileName.java")
    self.assertEqual(ctx.context_type, CONTEXT_TYPE.SOURCEFILE)
    self.assertTrue(ctx.match_mandatory)
    self.assertEqual(ctx.crc, "1234ABCD")

  def test_to_element_round_trip(self) -> None:
    original = Context(value="Homepage", context_type="linenumber", crc="DEADBEEF")
    element = original.to_element()
    parsed = Context(source_element=element)
    self.assertEqual(parsed.value, "Homepage")
    self.assertEqual(parsed.context_type, CONTEXT_TYPE.LINENUMBER)
    self.assertEqual(parsed.crc, "DEADBEEF")

  def test_validate_success(self) -> None:
    ctx = Context(value="Label", context_type=CONTEXT_TYPE.SOURCEFILE)
    self.assertTrue(ctx.validate())


class TestContextMalformedData(unittest.TestCase):
  def test_missing_value_raises(self) -> None:
    with self.assertRaises(ValueError):
      Context(context_type="sourcefile")  # type: ignore

  def test_missing_context_type_raises(self) -> None:
    with self.assertRaises(ValueError):
      Context(value="MyFile")  # type: ignore

  def test_invalid_enum_value_raises(self) -> None:
    with self.assertRaises(ValueError):
      Context(value="bad", context_type="not-a-context")  # type: ignore

  def test_invalid_type_in_validate(self) -> None:
    ctx = Context(value="ok", context_type="sourcefile")
    ctx.crc = 1234  # type: ignore
    with self.assertRaises(TypeError):
      ctx.validate()
