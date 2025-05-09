import pytest
from datetime import datetime
from enum import StrEnum
from types import SimpleNamespace
from lxml.etree import Element as LxmlElement
from xml.etree.ElementTree import Element as StdElement
from xliff import __FAKE__ELEMENT__
from xliff.utils import ensure_correct_element, ensure_usable_element, stringify


class DummyEnum(StrEnum):
  FOO = "foo"
  BAR = "bar"


class TestEnsureCorrectElement:
  def test_valid_tag_passes(self):
    el = LxmlElement("count")
    ensure_correct_element("count", el)  # Should not raise

  def test_fake_element_passes(self):
    # Uses a fake placeholder to bypass check
    ensure_correct_element("anything", __FAKE__ELEMENT__)  # Should not raise (bypassed)

  def test_invalid_tag_raises(self):
    el = StdElement("wrong")
    with pytest.raises(ValueError, match="Incorrect xml tag"):
      ensure_correct_element("expected", el)


class TestEnsureUsableElement:
  def test_lxml_element_is_usable(self):
    assert ensure_usable_element(LxmlElement("count")) is True

  def test_stdlib_element_is_usable(self):
    assert ensure_usable_element(StdElement("count")) is True

  def test_custom_object_with_required_attrs(self):
    obj = SimpleNamespace(tag="x", text="", tail="", attrib={})
    assert ensure_usable_element(obj) is True

  def test_missing_attribute_is_not_usable(self):
    obj = SimpleNamespace(tag="x", text="", tail="")  # no .attrib
    assert ensure_usable_element(obj) is False


class TestStringify:
  def test_string_value(self):
    assert stringify("hello") == "hello"

  def test_int_value(self):
    assert stringify(42) == "42"

  def test_float_value(self):
    assert stringify(3.14) == "3.14"

  def test_datetime_value(self):
    dt = datetime(2023, 5, 1, 15, 30)
    assert stringify(dt) == "20230501T153000Z"

  def test_enum_value(self):
    assert stringify(DummyEnum.FOO) == "foo"

  def test_unsupported_type_raises(self):
    with pytest.raises(NotImplementedError):
      stringify(object())
