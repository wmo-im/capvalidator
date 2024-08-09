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

from .validate import Validator

__version__ = '0.1.0-dev3'


class ValidationResult:
    def __init__(self, passed, message):
        self.passed = passed
        self.message = message


class DateResult:
    def __init__(self, sent, effective, onset, expiry):
        self.sent = sent
        self.effective = effective
        self.onset = onset
        self.expiry = expiry


def get_dates(cap) -> DateResult:
    """Interface to the date extraction method of the Validator class, which
    can be used in the API.

    Args:
        cap (bytes): The CAP alert XML file byte contents to be parsed.

    Returns:
        DateResult: The extracted date-time values.
    """
    dates = Validator(cap).get_dates()
    return DateResult(dates['sent'],
                      dates['effective'],
                      dates['onset'],
                      dates['expiry'])


def check_schema(cap) -> ValidationResult:
    """Interface to the schema validation method of the Validator class, which
    is used in the CLI.
    """
    passed, msg = Validator(cap).schema()
    return ValidationResult(passed, msg)


def check_signature(cap) -> ValidationResult:
    """Interface to the signature verification method of the Validator class,
    which is used in the CLI.
    """
    passed, msg = Validator(cap).signature()
    return ValidationResult(passed, msg)


def validate_xml(cap, strict=True) -> ValidationResult:
    """Performs the two steps of CAP validation: schema validation
    and signature verification.

    Args:
        cap (bytes): The CAP alert XML file byte contents to be validated.
        strict (bool): Whether to enforce an XML signature or not.
                        Defaults to True.

    Returns:
        ValidationResult: The validation status and the associated message
        justifying the status.
    """
    # Draft code to demonstrate the process of CAP validation

    schema_result = check_schema(cap)
    if not schema_result.passed:
        return schema_result

    signature_result = check_signature(cap)
    if not signature_result.passed:
        # In strict mode, fail if the signature is invalid
        if strict:
            return signature_result

        # Otherwise, pass but warn the user
        if signature_result.message == "CAP alert has not been signed.":
            warning = "CAP XML file is valid but has not been signed." + \
                        "Consider signing alerts in the future."
            return ValidationResult(True, warning)
        else:
            warning = "CAP XML file is valid but the signature is invalid." + \
                        "Consider signing alerts in the future."
            return ValidationResult(True, warning)

    return ValidationResult(True, "CAP XML file is valid.")
