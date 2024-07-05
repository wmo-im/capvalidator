import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XMLSchema
from io import StringIO


class CheckSchema:
    def __init__(self, cap):
        # ElementTree expects a file-like object
        self.cap = StringIO(cap)
        # Load the XML schema
        self.schema = XMLSchema('static/CAP-v1.2-schema.xsd')

    def validate(self):
        # Parse the XML document
        tree = ET.parse(self.cap)
        # Validate the XML document
        return tree.validate(self.schema)
