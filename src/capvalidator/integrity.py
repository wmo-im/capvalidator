from enum import Enum
import lxml.etree as ET
import hashlib
from base64 import b64encode

from .helpers import remove_signature, get_algorithm


class HashAlgorithms(Enum):
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
        # LXML requires the XML string to be encoded
        self.cap = cap.encode()

    def validate(self):
        """Checks the integrity of the CAP alert by comparing the hash
        value in the document with the calculated hash value.

        Returns:
            bool: The result of the comparison.
        """
        root = ET.fromstring(self.cap)
        namespace = {'ds': 'http://www.w3.org/2000/09/xmldsig#'}

        # Find the hash method and value
        algorithm = get_algorithm(root, 'digest')
        hash_value_element = root.find('.//ds:DigestValue', namespace)
        hash_value = hash_value_element.text

        # Calculate the hash of the CAP alert without the signature element
        alert = remove_signature(root)
        calculated_hash = self.calculate_hash(alert, algorithm)

        return hash_value == calculated_hash

    def calculate_hash(self, alert, algorithm):
        """Calculates the hash of the CAP alert based on the stated
        method in the document.

        Args:
            alert (str): The CAP alert string.
            algorithm (str): The link to the hash algorithm standard.

        Returns:
            str: The generated hash value.
        """
        print("Algorithm used: ", algorithm)
        h = HashAlgorithms[algorithm].value()
        # Encode the alert to bytes and update the hash object
        h.update(alert)
        digest = h.digest()
        base64_value = b64encode(digest).decode()
        return base64_value
