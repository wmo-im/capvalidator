from enum import Enum
import lxml.etree as ET
from base64 import b64decode
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

from .helpers import remove_signature, get_algorithm


class HashAlgorithms(Enum):
    ecdsa_sha224 = hashes.SHA224
    ecdsa_sha256 = hashes.SHA256
    ecdsa_sha384 = hashes.SHA384
    ecdsa_sha512 = hashes.SHA512
    ecdsa_sha3_224 = hashes.SHA3_224
    ecdsa_sha3_256 = hashes.SHA3_256
    ecdsa_sha3_384 = hashes.SHA3_384
    ecdsa_sha3_512 = hashes.SHA3_512


class CheckSignature:
    def __init__(self, cap):
        # LXML requires the XML string to be encoded
        self.cap = cap.encode()

    def validate(self):
        """Verifies the digital signature of the CAP alert.

        Returns:
            bool: The verification result.
        """
        root = ET.fromstring(self.cap)
        namespace = {'ds': 'http://www.w3.org/2000/09/xmldsig#'}

        # Extract certificate and public key
        certificate_element = root.find(
            './/ds:X509Certificate', namespaces=namespace)
        certificate = certificate_element.text

        public_key = self.get_public_key(certificate)

        # Extract signature and hash method used
        signature_element = root.find(
            './/ds:SignatureValue', namespaces=namespace)
        signature = signature_element.text

        algorithm = get_algorithm(root, 'signature')

        # Get the CAP alert without the signature element
        alert = remove_signature(root)

        return self.verify_signature(public_key, signature, algorithm, alert)

    def get_public_key(self, certificate):
        """Extracts the public key from the certificate.

        Args:
            certificate (str): The certificate string.

        Returns:
            VerifyingKey: The public key object extracted from the certificate.
        """
        if certificate is None:
            return None

        cert_bytes = b64decode(certificate)
        decoded_cert = x509.load_der_x509_certificate(cert_bytes)
        return decoded_cert.public_key()

    def verify_signature(self, public_key, signature, algorithm, alert):
        """Uses the public key fron the certificate to verify the
        XML signature.

        Args:
            public_key (cryptography.hazmat.primitives.asymmetric.dsa.DSAPublicKey): The public key to verify the signature. # noqa
            signature (str): The signature to verify.
            algorithm (str): The link to the hash algorithm standard.
            alert (bytes): The CAP alert without the signature.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        if public_key is None:
            return False

        algorithm_class = HashAlgorithms[algorithm].value
        signature_bytes = b64decode(signature)

        try:
            public_key.verify(
                signature_bytes, alert, padding.PKCS1v15(), ec.ECDSA(algorithm_class())
            )
            # If the signature is valid, the verify method returns None
            return True
        except InvalidSignature:
            return False
