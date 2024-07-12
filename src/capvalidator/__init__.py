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

from .schema import CheckSchema
from .integrity import CheckIntegrity
from .signature import CheckSignature

__version__ = '0.1.dev0'


class ValidationResult:
    def __init__(self, passed, message):
        self.passed = passed
        self.message = message


def check_schema(cap) -> bool:
    return CheckSchema(cap).validate()


def check_integrity(cap) -> bool:
    return CheckIntegrity(cap).validate()


def check_signature(cap) -> bool:
    return CheckSignature(cap).validate()


def validate_xml(cap) -> ValidationResult:
    """Performs the three steps of CAP validation: schema validation,
    integrity check, and signature verification.

    Args:
        cap (str): The CAP alert XML file contents to be validated.

    Returns:
        ValidationResult: The validation status and the associated message
        justifying the status.
    """
    # Draft code to demonstrate the process of CAP validation

    follows_schema = check_schema(cap)
    if not follows_schema:
        return ValidationResult(False, "CAP alert does not follow the schema.")

    hash_matches = check_integrity(cap)
    if not hash_matches:
        return ValidationResult(False, "CAP file digest value not found or it does match the alert content.")  # noqa

    signature_valid = check_signature(cap)
    if not signature_valid:
        return ValidationResult(False, "CAP file has not been signed or the signature is not valid.")  # noqa

    return ValidationResult(True, "CAP file is valid.")
