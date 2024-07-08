import enum
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
from io import StringIO
import hashlib
from base64 import b64encode


class HashAlgorithms(enum.Enum):
    sha1 = hashlib.sha1
    sha224 = hashlib.sha224
    sha256 = hashlib.sha256
    sha384 = hashlib.sha384
    sha512 = hashlib.sha512
    sha3_224 = hashlib.sha3_224
    sha3_256 = hashlib.sha3_256
    sha3_384 = hashlib.sha3_384
    sha3_512 = hashlib.sha3_512


class CheckIntegrity:
    def __init__(self, cap):
        # ElementTree expects a file-like object
        self.cap = StringIO(cap)

    def validate(self):
        tree = ET.parse(self.cap)
        root = tree.getroot()
        namespace = {'ds': 'http://www.w3.org/2000/09/xmldsig#'}

        # Find the hash method and value
        algorithm = root.find('.//ds:DigestMethod',
                              namespace).get('Algorithm')
        hash_value_element = root.find('.//ds:DigestValue', namespace)
        hash_value = hash_value_element.text if hash_value_element is not None else None  # noqa

        # Calculate the hash of the CAP alert
        alert = self.get_alert_string(root, namespace)
        calculated_hash = self.calculate_hash(alert, algorithm)

        print(f"Actual hash: {hash_value}")
        print(f"Calculate hash: {calculated_hash}")

        return hash_value == calculated_hash

    def get_alert_string(self, root, namespace):
        """Extracts the section of the XML without the signature
        and hash information.

        Args:
            root (Element): The root element of the XML document.
            namespace (dict): The digital signature namespace.

        Returns:
            str: The XML string without the signature and hash information.
        """
        signature_element = root.find('.//ds:Signature', namespace)

        if signature_element is None:
            return tostring(root)

        parent = signature_element.find('..')

        if parent is None:
            return ""

        # Remove the ds:Signature element from its parent
        parent.remove(signature_element)
        # Convert the modified tree back to a string
        return tostring(root, encoding='unicode')

    def calculate_hash(self, alert, algorithm):
        """Calculates the hash of the CAP alert based on the stated
        method in the document.

        Args:
            alert (str): The CAP alert string.
            algorithm (str): The link to the hash algorithm standard.

        Returns:
            str: The generated hash value.
        """
        name = algorithm.split('#')[-1]
        h = HashAlgorithms[name].value()
        # Encode the alert to bytes and update the hash object
        h.update(alert.encode())
        digest = h.digest()
        base64_value = b64encode(digest).decode()
        return base64_value
