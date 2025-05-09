import lxml.etree as ET
from xliff.objects import Count, CountGroup


def make_element(tag, attrib=None, text=None):
  el = ET.Element(tag, attrib=attrib or dict())
  el.text = text
  return el


class TestCount:
  def test_direct_init(self):
    c = Count(value=42, count_type="word", phase_name="translation", unit="word")
    assert c.value == 42
    assert c.count_type == "word"
    assert c.phase_name == "translation"
    assert c.unit == "word"

  def test_from_element(self):
    el = make_element(
      "count",
      {"count-type": "word", "phase-name": "translation", "unit": "word"},
      text="99",
    )
    c = Count(source_element=el)
    assert c.value == 99
    assert c.count_type == "word"
    assert c.phase_name == "translation"
    assert c.unit == "word"

  def test_to_element(self):
    c = Count(value=123, count_type="character")
    el = c.to_element(ET.Element)
    assert el.tag == "count"
    assert el.get("count-type") == "character"
    assert el.text == "123"


class TestCountGroup:
  def test_direct_init(self):
    counts = [Count(value=1, count_type="word"), Count(value=2, count_type="character")]
    cg = CountGroup(name="group1", counts=counts)
    assert cg.name == "group1"
    assert len(cg.counts) == 2
    assert cg.counts[0].value == 1

  def test_from_element(self):
    el = make_element("count-group", {"name": "metrics"})
    el.append(make_element("count", {"count-type": "word"}, text="11"))
    el.append(make_element("count", {"count-type": "character"}, text="22"))
    cg = CountGroup(source_element=el)
    assert cg.name == "metrics"
    assert len(cg.counts) == 2
    assert cg.counts[1].value == 22

  def test_to_element(self):
    cg = CountGroup(
      name="stats",
      counts=[Count(value=10, count_type="word"), Count(value=20, count_type="char")],
    )
    el = cg.to_element(ET.Element)
    assert el.tag == "count-group"
    assert el.get("name") == "stats"
    assert len(el) == 2
    assert el[0].tag == "count"
    assert el[0].text == "10"
    assert el[1].get("count-type") == "char"
