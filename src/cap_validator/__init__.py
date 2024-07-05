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

from cap_validator.validate_schema import CheckSchema
from cap_validator.verify_file import CheckIntegrity, VerifySignature

__version__ = '0.1.dev0'


class ValidationResult:
    def __init__(self, status, message):
        self.status = status
        self.message = message


def validate_cap(cap) -> ValidationResult:
    """Performs the three steps of CAP validation: schema validation,
    integrity check, and signature verification.

    Args:
        cap (str): The CAP alert XML file contents to be validated.

    Returns:
        ValidationResult: The validation status and the associated message
        justifying the status.
    """
    # Draft code to demonstrate the process of CAP validation

    follows_schema = CheckSchema(cap)
    if not follows_schema:
        return ValidationResult(False, "CAP alert does not follow the schema.")

    hash_matches = CheckIntegrity(cap)
    if not hash_matches:
        return ValidationResult(False, "CAP alert hash does not match the content.") # noqa

    signature_valid = VerifySignature(cap)
    if not signature_valid:
        return ValidationResult(False, "CAP alert has not been signed or the signature is not valid.") # noqa

    return ValidationResult(True, "CAP alert is valid.")
