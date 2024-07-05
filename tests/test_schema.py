from cap_validator.schema import CheckSchema


def test_valid_alert_schema(valid_alert):
    assert CheckSchema(valid_alert)


def test_no_identifier_schema(no_identifier):
    assert not CheckSchema(no_identifier)


def test_incorrect_digest_schema(incorrect_digest):
    assert CheckSchema(incorrect_digest)


def test_incorrect_signature_schema(incorrect_signature):
    assert CheckSchema(incorrect_signature)
