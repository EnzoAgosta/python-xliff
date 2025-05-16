import unittest
from xliff.errors import ValidationError
from xliff.objects import CountGroup, Count
from xliff.constants import COUNT_TYPE


class TestCountGroup(unittest.TestCase):
  def test_init_with_explicit_values(self) -> None:
    count1 = Count(value=5, count_type="total")
    count2 = Count(value=10, count_type="total")
    group = CountGroup(name="metrics", counts=[count1, count2])

    self.assertEqual(group.name, "metrics")
    self.assertEqual(len(group.counts), 2)
    self.assertIsInstance(group.counts[0], Count)
    self.assertEqual(group.counts[1].value, 10)

  def test_to_element_round_trip(self) -> None:
    counts = [Count(value=3, count_type="total"), Count(value=7, count_type="total")]
    group = CountGroup(name="summary", counts=counts)

    xml_element = group.to_element()
    parsed = CountGroup(source_element=xml_element)

    self.assertEqual(parsed.name, "summary")
    self.assertEqual(len(parsed.counts), 2)
    self.assertEqual(parsed.counts[0].value, 3)
    self.assertEqual(parsed.counts[1].count_type, COUNT_TYPE.TOTAL)

  def test_validate_success(self) -> None:
    group = CountGroup(
      name="valid-group",
      counts=[
        Count(value=1, count_type="total"),
        Count(value=2, count_type="total"),
      ],
    )
    group.validate(recurse=False)
    group.validate(recurse=True)


class TestCountGroupMalformedData(unittest.TestCase):
  def test_missing_name_raises(self) -> None:
    with self.assertWarns(UserWarning):
      group = CountGroup(counts=[Count(value=1, count_type="total")])  # type: ignore
    with self.assertRaises(ValidationError):
      group.validate()

  def test_non_string_name_raises_in_validate(self) -> None:
    group = CountGroup(name="valid", counts=[])
    group.name = 123  # type: ignore
    with self.assertRaises(ValidationError):
      group.validate()

  def test_invalid_child_in_validate_recurse(self) -> None:
    valid = Count(value=10, count_type="total")
    invalid = Count(value=10, count_type="total")
    invalid.unit = "invalid"  # type: ignore

    group = CountGroup(name="group", counts=[valid, invalid])
    with self.assertRaises(ValidationError):
      group.validate(recurse=True)
