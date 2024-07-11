from pkg_resources import resource_string
from lxml import etree as ET


class CheckSchema:
    def __init__(self, cap):
        # LXML requires the XML string to be encoded
        self.cap = cap.encode()

    def validate(self):
        """Validates the CAP alert against the CAP 1.2 schema.

        Returns:
            bool: The validation result.
        """
        parser = self.get_schema_parser()

        # Try to parse the CAP alert XML string.
        # If it fails, the XML is not valid.
        try:
            ET.fromstring(self.cap, parser)
            return True
        except ET.XMLSyntaxError:
            return False

    def get_schema_parser(self):
        """Performs the necessary steps to prepare the schema validator.

        Returns:
            XMLSchema: The schema validator object.
        """
        # Load the XSD schema
        schema_bytes = resource_string(__name__,
                                       "static/CAP-v1.2-schema.xsd"
                                       ).decode("utf-8")
        # Create the parser object
        schema_root = ET.XML(schema_bytes)
        schema = ET.XMLSchema(schema_root)
        return ET.XMLSchema(schema)
