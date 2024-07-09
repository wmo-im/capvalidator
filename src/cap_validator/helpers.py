import lxml.etree as ET


namespace = {'ds': 'http://www.w3.org/2000/09/xmldsig#'}


def remove_signature(root):
    """Extracts the section of the XML without the signature
    and hash information and then applies canonicalization.

    Args:
        root (Element): The root element of the XML document.

    Returns:
        str: The transformed XML byte string.
    """
    signature_element = root.find('.//ds:Signature', namespace)

    if signature_element is None:
        return ET.tostring(root, encoding='utf-8')

    # Get the parent of the ds:Signature element: the alert tag
    parent = signature_element.getparent()

    if parent is None:
        return b""

    # Remove the ds:Signature element from its parent
    parent.remove(signature_element)

    # Apply canonicalization (C14N 1.1) to the XML
    canonical_xml = ET.tostring(root, method="c14n2")
    return canonical_xml


def get_algorithm(root, type):
    """Extracts the hash algorithm used in the document.

    Args:
        root (Element): The root element of the XML document.

    Returns:
        str: The name of the algorithm, with hypens replaced by underscores.
    """
    match type:
        case 'signature':
            algorithm = root.find('.//ds:SignatureMethod',
                                  namespace).get('Algorithm')
        case 'digest':
            algorithm = root.find('.//ds:DigestMethod',
                                  namespace).get('Algorithm')
        case _:
            raise ValueError("Invalid algorithm type specified")

    name = algorithm.split('#')[-1]
    name = name.replace('-', '_')
    return name
