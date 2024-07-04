###############################################################################
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

import pytest
from cap_validator.validate_schema import CheckSchema
from cap_validator.verify_file import CheckIntegrity, VerifySignature


@pytest.fixture
def valid_alert():
    with open('data/seychelles.xml',
              'r', encoding='utf-8') as f:
        return f.read()


@pytest.fixture
def no_identifier():
    with open('data/no_identifier.xml',
              'r', encoding='utf-8') as f:
        return f.read()


@pytest.fixture
def incorrect_digest():
    with open('data/incorrect_digest.xml',
              'r', encoding='utf-8') as f:
        return f.read()


@pytest.fixture
def incorrect_signature():
    with open('data/incorrect_signature.xml',
              'r', encoding='utf-8') as f:
        return f.read()


def test_valid_alert(valid_alert):
    assert CheckSchema(valid_alert)
    assert CheckIntegrity(valid_alert)
    assert VerifySignature(valid_alert)


def test_no_identifier(no_identifier):
    assert not CheckSchema(no_identifier)
    assert not CheckIntegrity(no_identifier)
    assert VerifySignature(no_identifier)


def test_incorrect_digest(incorrect_digest):
    assert CheckSchema(incorrect_digest)
    assert not CheckIntegrity(incorrect_digest)
    assert VerifySignature(incorrect_digest)


def test_incorrect_signature(incorrect_signature):
    assert CheckSchema(incorrect_signature)
    assert CheckIntegrity(incorrect_signature)
    assert not VerifySignature(incorrect_signature)
