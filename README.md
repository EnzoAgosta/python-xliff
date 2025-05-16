# WORK IN PROGRESS! CONTRIBUTIONS AND HELP WELCOME BUT NOWHERE NEAR READY FOR USE YET 

# Python-XLIFF

**Safe, Easy, and Fast XLIFF 1.2 Handling for Python**

Python-XLIFF is a modern Python library designed to make working with
[XLIFF 1.2](https://docs.oasis-open.org/xliff/v1.2/os/xliff-core.html) files safer,
easier, and faster. It provides a strongly-typed, spec-compliant, and Pythonic
interface to read, create, manipulate, and serialize XLIFF files using any XML library
of your choice.

## ✨ Features

- 🔐 **Spec-Strict**: Enforces full XLIFF 1.2 compliance — no more malformed or invalid
XLIFF structures.
- 🐍 **Pythonic API**: Use dot notation and native python objects like datetime and
enums to manipulate elements.
- 🔄 **Interoperable**: Works with any XML library (e.g., `xml.etree.ElementTree`,
`lxml`, etc.) via a simple adapter protocol.
- 🧱 **Modular and Typed**: Each XLIFF element is represented as a well-defined Python
class with strict and detailled type hints.
- 📤 **Serialization & Deserialization**: Convert between Python objects and XML
Elements with ease.

## 🚀 Quick Start

```bash
pip install python-xliff
```
OR
```bash
uv add python-xliff
```

### Parsing an Existing XLIFF Element

```python
from xliff import TransUnit
import xml.etree.ElementTree as ET

element = ET.fromstring('<trans-unit id="1"><source>Hello</source></trans-unit>')
trans_unit = TransUnit(source_element=element)

print(trans_unit.source.text)  # Output: Hello
trans_unit.target = "Bonjour"
```

### Creating an XLIFF Tree from Scratch

```python
from xliff import Xliff, File, Body, TransUnit
from xml.etree.ElementTree import Element

xliff = Xliff(
    version="1.2",
    files=[
        File(
            original="example.txt",
            source_language="en",
            target_language="fr",
            body=Body(
                trans_units=[
                    TransUnit(id="1", source="Hello", target="Bonjour")
                ]
            )
        )
    ]
)

lxml_element = xliff.to_element()  # Convert to lxml.etree.Element by default
python_xml_element = xliff.to_element(Element)  # Convert to xml.etree.ElementTree.Element by simply passing it as the factory
```

## ✅ Why Use Python-XLIFF?

- Save time and reduce bugs with a clean, intuitive API
- Guarantee standards compliance for translators and CAT tools
- Easily validate, test, and manipulate files in pipelines or applications
- Use your preferred XML backend

## 📚 Specification Support

This library fully adheres to the
[XLIFF 1.2 specification](https://docs.oasis-open.org/xliff/v1.2/os/xliff-core.html),
including all required and optional attributes, structural constraints, and content models.

## 🔧 Roadmap

- 🔧 Support for all elements and attributes in the spec
    - 🔧 Named groups
    - 🔜 Top-level and Header Elements
    - 🔜 Structural Elements
    - 🔜 Inline Elements
    - 🔜 Delimiter Element
- 🔜 support for Path/File like objects
- 🔜 Validation only functions for quick analysis
- 🔜 CLI version

## 💬 Contributing

Contributions and feedback are welcome! See `CONTRIBUTING.md` for details.

## 🛡 License

MIT License — see `LICENSE` for full text.