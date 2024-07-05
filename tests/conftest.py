import pytest


@pytest.fixture
def valid_alert():
    with open('data/seychelles.xml', 'r', encoding='utf-8') as f:
        return f.read()


@pytest.fixture
def no_identifier():
    with open('data/no_identifier.xml', 'r', encoding='utf-8') as f:
        return f.read()


@pytest.fixture
def incorrect_digest():
    with open('data/incorrect_digest.xml', 'r', encoding='utf-8') as f:
        return f.read()


@pytest.fixture
def incorrect_signature():
    with open('data/incorrect_signature.xml', 'r', encoding='utf-8') as f:
        return f.read()
