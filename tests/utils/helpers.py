import os
from glob import glob


def get_fixtures():
    """Obtain and categorise the automatic fixture names
    from the data directory.

    Returns:
        tuple: A tuple containing four lists of fixture names, each
        corresponding to a different category of CAP XML file to test.
    """
    # Data for testing
    data_dir = 'tests/data'

    # Find all XML files within this data directory
    xml_files = glob(os.path.join(data_dir, '**/*.xml'))

    # Initialise the four fixture categories
    valid_fixtures, invalid_schema_fixtures, invalid_signature_fixtures, no_signature_fixtures = [], [], [], []  # noqa

    for file_path in xml_files:
        # Create the fixture name based on the path and XML file name,
        # e.g. sc/valid.xml -> sc_valid
        name = os.path.relpath(file_path, data_dir).replace(
            os.path.sep, '_').replace('.xml', '').replace('.', '_')

        if '_valid' in name:
            valid_fixtures.append(name)
        if 'schema' in name:
            invalid_schema_fixtures.append(name)
        elif 'invalid' in name:
            invalid_signature_fixtures.append(name)
        elif 'no_signature' in name:
            no_signature_fixtures.append(name)

    return valid_fixtures, invalid_schema_fixtures, invalid_signature_fixtures, no_signature_fixtures  # noqa
