import lxml.etree as ET
from xliff.objects import Count, CountGroup
from xliff.constants import COUNT_TYPE, UNIT


def make_element(tag, attrib=None, text=None):
  el = ET.Element(tag, attrib=attrib or dict())
  el.text = text
  return el


class TestCount:
  def test_direct_init(self):
    c = Count(
      value=42, count_type=COUNT_TYPE.TOTAL, phase_name="translation", unit=UNIT.WORD
    )
    assert c.value == 42
    assert c.count_type == COUNT_TYPE.TOTAL
    assert c.phase_name == "translation"
    assert c.unit == UNIT.WORD

  def test_from_element(self):
    el = make_element(
      "count",
      {"count-type": "repetition", "phase-name": "translation", "unit": "character"},
      text="99",
    )
    c = Count(source_element=el)
    assert c.value == 99
    assert c.count_type == COUNT_TYPE.REPETITION
    assert c.phase_name == "translation"
    assert c.unit == UNIT.CHARACTER

  def test_to_element(self):
    c = Count(value=123, count_type=COUNT_TYPE.NUM_USAGE)
    el = c.to_element(ET.Element)
    assert el.tag == "count"
    assert el.get("count-type") == COUNT_TYPE.NUM_USAGE.value
    assert el.text == "123"


class TestCountGroup:
  def test_direct_init(self):
    counts = [
      Count(value=1, count_type=COUNT_TYPE.TOTAL, unit=UNIT.WORD),
      Count(value=2, count_type=COUNT_TYPE.REPETITION, unit=UNIT.CHARACTER),
    ]
    cg = CountGroup(name="group1", counts=counts)
    assert cg.name == "group1"
    assert len(cg.counts) == 2
    assert cg.counts[0].value == 1
    assert cg.counts[0].unit == UNIT.WORD

  def test_from_element(self):
    el = make_element("count-group", {"name": "metrics"})
    el.append(make_element("count", {"count-type": "total", "unit": "word"}, text="11"))
    el.append(
      make_element("count", {"count-type": "num-usage", "unit": "character"}, text="22")
    )
    cg = CountGroup(source_element=el)
    assert cg.name == "metrics"
    assert len(cg.counts) == 2
    assert cg.counts[1].value == 22
    assert cg.counts[1].count_type == COUNT_TYPE.NUM_USAGE

  def test_to_element(self):
    cg = CountGroup(
      name="stats",
      counts=[
        Count(value=10, count_type=COUNT_TYPE.TOTAL, unit=UNIT.LINE),
        Count(value=20, count_type=COUNT_TYPE.REPETITION, unit=UNIT.CHARACTER),
      ],
    )
    el = cg.to_element(ET.Element)
    assert el.tag == "count-group"
    assert el.get("name") == "stats"
    assert len(el) == 2
    assert el[0].tag == "count"
    assert el[0].text == "10"
    assert el[1].get("count-type") == COUNT_TYPE.REPETITION.value
