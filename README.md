# nates-useful-functions-python-module (nuf)

A versatile, multi-file utility module that aggregates a series of useful Python code referenced repeatedly across various projects. 

## Package Structure

The package is structured as follows under the `src` directory:
- `src/nuf/__init__.py`: Initializes the package and dynamically imports all Python files/modules in its directory.
- `src/nuf/core.py`: Core functionality.
- `src/nuf/file_utils.py`: Utilities for working with files.
- `src/nuf/message_utils.py`: Utilities for messaging and logs.
- `src/nuf/format_utils.py`: Utilities for formatting and time conversions.

## Dynamic Importing

This module automatically discovers and imports all Python files present inside the `src/nuf/` folder. When you add a new Python file (e.g. `src/nuf/new_helper.py`), it is automatically available as `nuf.new_helper` without needing to modify `__init__.py`.

## Usage

Here is a quick example of how to import and use the package:

```python
import nuf

# Access functions from core.py
print(nuf.core.core_func())

# Access functions from file_utils.py
print(nuf.file_utils.file_func())

# Access functions from message_utils.py
print(nuf.message_utils.message_func())
```

## Running Tests

To run the local verification test suite, run:

```bash
python test_nuf.py
```
