import os
from glob import glob


def get_fixtures():
    # Data for testing
    data_dir = 'tests/data'

    # Find all XML files within this data directory
    xml_files = glob(os.path.join(data_dir, '**/*.xml'))

    # Initialise the five fixture categories
    valid_fixtures, invalid_schema_fixtures, invalid_integrity_fixtures, invalid_signature_fixtures = [], [], [], []  # noqa

    for file_path in xml_files:
        # Create the fixture name based on the path and XML file name,
        # e.g. sc/valid.xml -> sc_valid
        name = os.path.relpath(file_path, data_dir).replace(
            os.path.sep, '_').replace('.xml', '').replace('.', '_')

        if 'valid' in name:
            valid_fixtures.append(name)
        elif 'no' in name:
            invalid_schema_fixtures.append(name)
        elif 'digest' in name:
            invalid_integrity_fixtures.append(name)
        elif 'signature' in name:
            invalid_signature_fixtures.append(name)

    return valid_fixtures, invalid_schema_fixtures, invalid_integrity_fixtures, invalid_signature_fixtures # noqa
