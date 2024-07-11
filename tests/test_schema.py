from capvalidator.schema import CheckSchema


def test_valid_alert_schema(valid_alert):
    follows_schema = CheckSchema(valid_alert).validate()
    assert follows_schema


def test_no_identifier_schema(no_identifier):
    follows_schema = CheckSchema(no_identifier).validate()
    assert not follows_schema


def test_incorrect_digest_schema(incorrect_digest):
    follows_schema = CheckSchema(incorrect_digest).validate()
    assert follows_schema


def test_incorrect_signature_schema(incorrect_signature):
    follows_schema = CheckSchema(incorrect_signature).validate()
    assert follows_schema
