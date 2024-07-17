import pytest
import os
from glob import glob

# Data for testing
data_dir = 'tests/data'

# Find all XML files within this data directory
xml_files = glob(os.path.join(data_dir, '**/*.xml'))


def generate_fixture(file_path):
    @pytest.fixture()
    def xml_fixture(scope='module'):
        """Contains the contents of the XML file."""
        print(f"Loading fixture: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return xml_fixture


def inject_fixture(name, file_path):
    """Generates the pytest fixture and injects it into the global namespace.

    Args:
        name (str): The fixture name to be referenced in the test functions.
        file_path (str): The path to the XML file to be loaded.
    """
    globals()[name] = generate_fixture(file_path)


for file_path in xml_files:
    # Create the fixture name based on the path and XML file name,
    # e.g. sc/valid.xml -> sc_valid
    fixture_name = os.path.relpath(file_path, data_dir).replace(
        os.path.sep, '_').replace('.xml', '').replace('.', '_')

    # Dynamically create a fixture for each XML file
    inject_fixture(fixture_name, file_path)
