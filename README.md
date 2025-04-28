# PyETR

## Documentation

Please see the documentation page [here](https://oxford-hai-lab.github.io/PyETR/)

## Installation

Make sure you have [python 3.11 or above](https://www.python.org/downloads/) and [poetry](https://python-poetry.org/docs/#installation) installed

Then just run:

`poetry install`

## Testing

For a test program, enter the tests directory and run:

`poetry run pytest -n auto`

For more advanced tests:

`poetry run pytest -n auto --viewops`

For coverage of pyetr (from tests folder):

`poetry run pytest -n 8 --viewops --cov=../pyetr/ --cov-report=term-missing`
