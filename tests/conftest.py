import pytest
import os
from glob import glob

# Data for testing
data_dir = 'tests/data'

# Find all XML files within this data directory
xml_files = glob(os.path.join(data_dir, '**/*.xml'))


def load_xml_file(file_path):
    """Helper function to load and return the contents of an XML file.

    Args:
        file_path (str): The path to the XML file to load.

    Returns:
        str: The XML contents.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


for file_path in xml_files:
    # Create the fixture name based on the path and XML file name,
    # e.g. sc/valid.xml -> sc_valid
    fixture_name = os.path.relpath(file_path, data_dir).replace(
        os.path.sep, '_').replace('.xml', '').replace('.', '_')

    def _fixture_function(file_path=file_path):
        return load_xml_file(file_path)

    # Dynamically create a fixture for each XML file
    globals()[fixture_name] = pytest.fixture(
        name=fixture_name)(_fixture_function)
