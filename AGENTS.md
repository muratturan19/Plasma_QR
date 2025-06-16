# Repository Guidelines

This file provides rules for contributors working on this project.

## Code Style
- Follow [PEP 8](https://peps.python.org/pep-0008/) conventions.
- Use four spaces for indentation and keep lines under 100 characters.
- Include type hints for public functions and methods.
- Document public classes and functions with meaningful docstrings.

## Testing Requirements
- Add unit tests for new features in a `tests/` directory mirroring the package layout.
- Use Python's standard `unittest` framework.
- Ensure all tests pass with `python -m unittest discover` before committing.

## New Module Conventions
- Each package should contain an `__init__.py` file.
- New modules should have a module-level docstring describing their purpose.
- Prefer relative imports within packages.
- Keep class and function names descriptive and in English.

