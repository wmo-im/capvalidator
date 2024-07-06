from pkg_resources import resource_string
from lxml import etree as ET


class CheckSchema:
    def __init__(self, cap):
        # LXML requires the XML string to be encoded
        self.cap = cap.encode()
        # Load the XSD schema
        self.schema = resource_string(__name__,
                                      "static/CAP-v1.2-schema.xsd"
                                      ).decode("utf-8")

    def get_schema_parser(self):
        schema_root = ET.XML(self.schema)
        return ET.XMLSchema(schema_root)

    def validate(self):
        parser = ET.XMLParser(schema=self.get_schema_parser())

        # Try to parse the CAP alert XML string.
        # If it fails, the XML is not valid.
        try:
            ET.fromstring(self.cap, parser)
            return True
        except ET.XMLSyntaxError:
            return False
