import enum
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
from io import StringIO
import hashlib
from base64 import b64encode, b64decode
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


class HashAlgorithms(enum.Enum):
    sha256 = hashlib.sha256
    ecdsa_sha256 = hashes.SHA256


class CheckIntegrity:
    def __init__(self, cap):
        # ElementTree expects a file-like object
        self.cap = StringIO(cap)

    def __call__(self):
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
        hash_function = HashAlgorithms[name].value()
        hash_value = hash_function(alert).digest()
        hash_value = b64encode(hash_value).decode()
        return hash_value


class VerifySignature:
    def __init__(self, cap):
        # ElementTree expects a file-like object
        self.cap = StringIO(cap)

    def __call__(self):
        tree = ET.parse(self.cap)
        root = tree.getroot()
        namespace = {'ds': 'http://www.w3.org/2000/09/xmldsig#'}

        # Extract certificate and public key
        certificate_element = root.find(
            './/ds:X509Certificate', namespaces=namespace)
        certificate = certificate_element.text if certificate_element is not None else None  # noqa

        public_key = self.get_public_key(certificate)

        # Extract signature and hash method used
        signature_element = root.find(
            './/ds:SignatureValue', namespaces=namespace)
        signature = signature_element.text if signature_element is not None else None  # noqa

        algorithm = root.find(
            './/ds:SignatureMethod', namespaces=namespace
        ).get('Algorithm')

        return self.verify_signature(public_key, signature, algorithm)

    def get_public_key(self, certificate):
        """Extracts the public key from the certificate.

        Args:
            certificate (str): The certificate string.

        Returns:
            VerifyingKey: The public key extracted from the certificate.
        """
        cert_bytes = b64decode(certificate)
        decoded_cert = x509.load_der_x509_certificate(cert_bytes)
        return decoded_cert.public_key()

    def verify_signature(self, public_key, signature, algorithm):
        """Uses the public key fron the certificate to verify the
        XML signature.

        Args:
            public_key (cryptography.hazmat.primitives.asymmetric.dsa.DSAPublicKey): The public key to verify the signature. # noqa
            signature (str): The signature to verify.
            algorithm (str): The link to the hash algorithm standard.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        name = algorithm.split('#')[-1]
        algorithm_function = HashAlgorithms[name].value()
        signature_bytes = b64decode(signature)
        try:
            # TODO: Add the encoded data as the 2nd argument to the verify method
            public_key.verify(
                signature=signature_bytes,
                algorihtm=algorithm_function
            )
            # If the signature is valid, the verify method returns None
            return True
        except InvalidSignature:
            return False
