import unittest
from xliff.objects import Count
from xliff.constants import COUNT_TYPE, UNIT


class TestCount(unittest.TestCase):
  def test_init_with_explicit_values(self) -> None:
    count = Count(value=42, count_type="total", phase_name="phase1", unit="word")
    self.assertEqual(count.value, 42)
    self.assertEqual(count.count_type, COUNT_TYPE.TOTAL)
    self.assertEqual(count.phase_name, "phase1")
    self.assertEqual(count.unit, UNIT.WORD)

  def test_to_element_round_trip(self) -> None:
    count = Count(value=10, count_type=COUNT_TYPE.TOTAL)
    element = count.to_element()
    restored = Count(source_element=element)
    self.assertEqual(restored.value, 10)
    self.assertEqual(restored.count_type, COUNT_TYPE.TOTAL)

  def test_validate_success(self) -> None:
    count = Count(value=100, count_type=COUNT_TYPE.TOTAL)
    self.assertTrue(count.validate())


class TestCountMalformedData(unittest.TestCase):
  def test_missing_value_raises(self) -> None:
    with self.assertRaises(ValueError):
      Count(count_type="total")  # type: ignore

  def test_missing_count_type_raises(self) -> None:
    with self.assertRaises(ValueError):
      Count(value=1)  # type: ignore

  def test_invalid_count_type_raises(self) -> None:
    with self.assertRaises(ValueError):
      Count(value=5, count_type="not-a-type")

  def test_invalid_unit_type_raises(self) -> None:
    with self.assertRaises(ValueError):
      Count(value=5, count_type="total", unit="invalid-unit")

  def test_invalid_type_in_validate(self) -> None:
    count = Count(value=5, count_type="total")
    count.unit = "not-a-unit"  # type: ignore
    with self.assertRaises(TypeError):
      count.validate()
