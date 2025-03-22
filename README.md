# Stadtreinigung Hamburg

[![PyPI](https://img.shields.io/pypi/v/stadtreinigung-hamburg.svg?logo=python&logoColor=white)](https://pypi.org/project/stadtreinigung-hamburg/)

This library provides access to garbage collection dates
in Hamburg. It scrapes the official website of Stadtreinigung Hamburg,
so this library can break at any time. Please open an issue if the
library does not work anymore.

## Installation

Using pip:

```
pip install stadtreinigung-hamburg
```

Using uv:

```
uv pip install stadtreinigung-hamburg
```

## Usage

After installing, use the terminal to run the program:

```
stadtreinigung_hamburg Sesamstraße 123
```


If your street name has a space, wrap the street in quotes:

```
stadtreinigung_hamburg "Sesame Street" 123
```


If you have problems with the street or street number,
use the official website and get the collection dates.
Then, search for `asId` and `hnId`. Those are the IDs for
your street and street number. You can use them too:

```
stadtreinigung_hamburg --asid 1234 --hnid 99999
```

Or mix it:

```
stadtreinigung_hamburg Sesamstraße --hnid 99999
```

## Development

This project uses [uv](https://github.com/astral-sh/uv) for dependency management and packaging.

### Setup Development Environment

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment and install dependencies
uv venv
uv pip install -e .
```

### Building the package

```bash
uv build
```

### Publishing to PyPI

This project uses GitHub Actions with trusted publishing to automatically release to PyPI when a new GitHub release is created. The workflow uses PyPI's trusted publisher mechanism, which means no API tokens need to be stored in GitHub secrets.

To set up trusted publishing:

1. Go to PyPI and navigate to your project
2. Go to "Settings" > "Publishing"
3. Add a new publisher with:
   - Publisher: GitHub Actions
   - Organization: your-github-username
   - Repository: stadtreinigung_hamburg
   - Workflow name: Publish Python Package

Once configured, creating a new release on GitHub will automatically trigger a build and publish to PyPI.

#### Version Management

The package version is automatically set to match the GitHub release tag. When creating a new release:

1. Use semantic versioning for your tag (e.g., `v1.0.0`, `v1.0.1`)
2. The GitHub Action will extract the version number from the tag and update the package version before publishing

For local publishing (if you have the necessary permissions):

```bash
uv build
uv publish
```
