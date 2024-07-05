from cap_validator import validate_cap, ValidationResult


def test_valid_alert_main(valid_alert):
    assert validate_cap(valid_alert) == ValidationResult(
        True, "CAP alert is valid.")


def test_no_identifier_main(no_identifier):
    assert validate_cap(no_identifier) == ValidationResult(
        False, "CAP alert does not follow the schema.")


def test_incorrect_digest_main(incorrect_digest):
    assert validate_cap(incorrect_digest) == ValidationResult(
        False, "CAP alert hash does not match the content.")


def test_incorrect_signature_main(incorrect_signature):
    assert validate_cap(incorrect_signature) == ValidationResult(
        False, "CAP alert has not been signed or the signature is not valid.")
