# The CAP Validator

### The Python module for ensuring the validity of CAP alerts.

<div align="center">

  <a href="https://github.com/wmo-im/capvalidator/blob/main/LICENSE" alt="License" ><img src="https://img.shields.io/badge/License-Apache_2.0-blue" alt="License Badge"></img></a>
  [![Super-Linter](https://github.com/wmo-im/capvalidator/actions/workflows/test-code-quality.yml/badge.svg)](https://github.com/marketplace/actions/super-linter)
  ![Unit-Tests](https://github.com/wmo-im/capvalidator/actions/workflows/unit-tests.yml/badge.svg)
  ![Publish-To-PyPI](https://github.com/wmo-im/capvalidator/actions/workflows/publish-to-pypi.yml/badge.svg)

</div>

## Features

- **Schema Validation**: Ensure your CAP XML file follows the [CAP v1.2 standard](https://docs.oasis-open.org/emergency/cap/v1.2/CAP-v1.2-os.html).
- **Digital Signature Validation**: Verify that the CAP XML file comes from a legitimate source and has not been tampered with.

*Note: Currently, only certificates issued by a trused certificate authority (CA) are supported. This means signatures with a self-signed certificate will **not** pass the validation.*

## Getting Started

### 1. Installation

```bash
pip install capvalidator
```

### 2A. Using the API

We can perform a total validation of the CAP XML file using `validate_xml(cap, strict)`.

- `cap`: The CAP alert XML byte string.
- `strict`: Whether or not signature validation is enforced. Defaults to `True`.

```python
from capvalidator import validate_xml

# Read the CAP XML file as a byte string
with open(<cap-file-directory>, "rb") as f:
    cap = f.read()

# Perform the validation
result = validate_xml(cap, strict=True)

# Check the result
passed = result.passed
msg = result.msg

if not passed:
    # Logic for handling invalid CAP file

# Logic for handling valid CAP file
```

Or, alternatively, we can perform a more refined validation using `check_schema(cap)` and/or `check_signature(cap)`:
```python
from capvalidator import check_schema, check_signature

# Read the CAP XML file as a byte string
with open(<cap-file-directory>, "rb") as f:
    cap = f.read()

# Validate the schema
schema_result = check_schema(cap)

# Check the results
passed = schema_result.passed
msg = schema_result.msg

if not passed:
    # Logic for handling invalid CAP file

# Validate the signature
signature_result = check_signature(cap)

# Check the results
passed = signature_result.passed
msg = signature_result.msg

if not passed:
    # Logic for handling invalid CAP file

# Logic for handling valid CAP file

```

There is also a date extractor `get_dates(cap)` which you may find useful:
```python
from capvalidator import get_dates

# Read the CAP XML file as a byte string
with open(<cap-file-directory>, "rb") as f:
    cap = f.read()

dts = get_dates(cap)

sent_date = dts.sent
effective_date = dts.effective
onset_date = dts.onset
expiry_date = dts.expiry
```

### 2B. Using the CLI

We can perform a total validation of the CAP XML file:

```bash
capvalidator validate <cap-file-directory>
```
By default this includes schema and signature validation.

To manually enable/disable enforcement of a valid XML signature, we can use the `--strict` or `--no-strict` arguments respectively:

```bash
capvalidator validate --strict <cap_file-directory> 
```

```bash
capvalidator validate --no-strict <cap_file-directory> 
```

Or, alternatively, for more refined validations we can use the `--type` argument:
```bash
capvalidator validate --type schema <cap-file-directory>
```

```bash
capvalidator validate --type signature <cap-file-directory>
```

## Bugs and Issues

All bugs, enhancements and issues are managed on [GitHub](https://github.com/wmo-im/capvalidator/issues).

## Contact

* [Rory Burke](https://github.com/RoryPTB)
