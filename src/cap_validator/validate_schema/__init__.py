import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XMLSchema
from io import StringIO


class CheckSchema:
    def __init__(self, cap):
        # ElementTree expects a file-like object
        self.cap = StringIO(cap)

    def __call__(self):
        # Load the XML schema
        schema = XMLSchema('CAP-v1.2-schema.xsd')
        # Parse the XML document
        tree = ET.parse(self.cap)
        # Validate the XML document
        return tree.validate(schema)
