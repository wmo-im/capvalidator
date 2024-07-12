import pytest
from .helpers import get_fixtures
from capvalidator import validate_xml, ValidationResult


valid_fixtures, invalid_schema_fixtures, invalid_integrity_fixtures, invalid_signature_fixtures = get_fixtures()  # noqa

expected_results = []

for fixture in valid_fixtures:
    result = ValidationResult(True, "CAP file is valid.")
    expected_results.append((fixture, result))

for fixture in invalid_schema_fixtures:
    result = ValidationResult(False, "CAP alert does not follow the schema.")
    expected_results.append((fixture, result))

for fixture in invalid_integrity_fixtures:
    result = ValidationResult(False, "CAP file digest value not found or it does match the alert content.")  # noqa
    expected_results.append((fixture, result))

for fixture in invalid_signature_fixtures:
    result = ValidationResult(False, "CAP file has not been signed or the signature is not valid.")  # noqa
    expected_results.append((fixture, result))


# Define the pytest_generate_tests hook to generate tests dynamically
def pytest_generate_tests(metafunc):
    if 'fixture' in metafunc.fixturenames:
        # Generate test cases based on the expected results array
        metafunc.parametrize('fixture,expected_output', expected_results)


# Define the actual test function
def test_validate_xml(cap, expected_output):
    # Perform the validation
    result = validate_xml(cap)

    # Check the result
    assert result.passed == expected_output.passed
    assert result.message == expected_output.message
