# Egyptian National ID

[![PyPI version](https://img.shields.io/pypi/v/egyid.svg)](https://pypi.org/project/egyid/)
[![Python versions](https://img.shields.io/pypi/pyversions/egyid.svg)](https://pypi.org/project/egyid/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/Petter0x1/egyid/actions/workflows/ci.yml/badge.svg)](https://github.com/Petter0x1/egyid/actions)

A lightweight and comprehensive Python library for validating, parsing, and generating Egyptian National ID numbers. Built with type hints and designed for reliability in production environments.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## Features

- **Validation**: Comprehensive ID validation including checksum verification, date validation, and governorate checks
- **Parsing**: Extract birth date, gender, age, governorate, and region information from ID numbers
- **Generation**: Create valid mock Egyptian National IDs for testing and development
- **Type Safety**: Full type hints for better IDE support and code reliability
- **Arabic Support**: Handles Arabic numerals in ID input
- **Cross-Platform**: Compatible with Python 3.8+

## Installation

### From PyPI (Recommended)

```bash
pip install egyid
```

### From Source

```bash
git clone https://github.com/Petter0x1/egyid.git
cd egyid
pip install .
```

### Requirements

- Python 3.8 or higher
- No external dependencies

## Quick Start

```python
from egyid import EgyptianNationalId

# Validate an ID
is_valid = EgyptianNationalId.is_valid_id("29010280165195")
print(is_valid)  # True

# Parse an ID
eid = EgyptianNationalId("29010280165195")
if eid.is_valid():
    print(f"Birth Date: {eid.birth_date}")  # 1990-10-28
    print(f"Gender: {eid.gender}")          # male
    print(f"Governorate: {eid.governorate}") # Cairo
    print(f"Age: {eid.age}")                # 35 (as of 2026)
    print(f"Region: {eid.region_name}")     # Cairo

# Generate a new ID
new_id = EgyptianNationalId.generate({
    "year": 1995,
    "gender": "female",
    "governorate": "01"  # Cairo
})
print(new_id)  # e.g., "39501010100000" (with correct checksum)

# Get full information as dictionary
info = eid.to_dict()
print(info)
# {
#     "nationalId": "29010280165195",
#     "birthYear": 1990,
#     "birthMonth": 10,
#     "birthDay": 28,
#     "age": 35,
#     "gender": "male",
#     "governorate": "Cairo",
#     "region": "Cairo",
#     "insideEgypt": true,
#     "isAdult": true
# }
```

## API Reference

### Class: `EgyptianNationalId`

#### Methods

- `EgyptianNationalId(id_value: Union[str, int])` - Create an instance from an ID string or integer
- `is_valid() -> bool` - Check if the ID is valid
- `to_dict() -> Optional[Dict[str, Any]]` - Return ID information as a dictionary (None if invalid)

#### Properties

- `birth_date: Optional[date]` - Birth date
- `age: Optional[int]` - Current age
- `gender: str` - 'male' or 'female'
- `governorate: Optional[str]` - Governorate name
- `region_name: str` - Region name

#### Class Methods

- `is_valid_id(id_value: Union[str, int]) -> bool` - Validate without creating instance
- `generate(options: Optional[Dict[str, Any]] = None) -> str` - Generate a new valid ID
- `parse(id_value: Union[str, int]) -> EgyptianNationalId` - Alias for constructor
- `check_is_male(id_value: Union[str, int]) -> bool` - Check if ID belongs to male
- `check_is_female(id_value: Union[str, int]) -> bool` - Check if ID belongs to female
- `check_is_adult(id_value: Union[str, int]) -> bool` - Check if person is 18+

### Generation Options

The `generate()` method accepts an optional dictionary with:
- `year: int` - Birth year (default: random 1950-current)
- `month: int` - Birth month (default: random 1-12)
- `day: int` - Birth day (default: valid for month/year)
- `gender: str` - 'male' or 'female' (default: random)
- `governorate: str` - 2-digit governorate code (default: random)

## Testing

Run the test suite:

```bash
python -m unittest discover tests
```

Tests cover validation, parsing, generation, and edge cases across all supported Python versions.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/Petter0x1/egyid.git
cd egyid
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -e .
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

@Petter0x1
