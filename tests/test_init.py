import pytest
import os
from glob import glob
from capvalidator import validate_xml, ValidationResult

###############################################################################
# Obtain and categorise the automatic fixtures from the data directory


def get_fixtures():
    # Data for testing
    data_dir = 'tests/data'

    # Find all XML files within this data directory
    xml_files = glob(os.path.join(data_dir, '**/*.xml'))

    # Initialise the five fixture categories
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


valid_fixtures, invalid_schema_fixtures, invalid_signature_fixtures, no_signature_fixture = get_fixtures()  # noqa

###############################################################################
# Define the expected test results for each fixture category

expected_results = []

for fixture in valid_fixtures:
    result = ValidationResult(True, "CAP XML file is valid.")
    expected_results.append((fixture, result))

for fixture in invalid_schema_fixtures:
    result = ValidationResult(False,
                              "CAP alert does not follow the CAP v1.2 schema.")
    expected_results.append((fixture, result))

for fixture in invalid_signature_fixtures:
    result = ValidationResult(False, "CAP alert signature is invalid or the data has been tampered with.")  # noqa
    expected_results.append((fixture, result))

for fixture in no_signature_fixture:
    result = ValidationResult(False, "CAP alert has not been signed.")
    expected_results.append((fixture, result))

###############################################################################
# Use the input data and expected result pair to create the test cases


@pytest.mark.parametrize("cap, expected_output", expected_results)
def test_validate_xml(cap, expected_output):
    print(cap)
    
    # Perform the validation
    result = validate_xml(cap)

    # Check the result
    assert result.passed == expected_output.passed
    assert result.message == expected_output.message
