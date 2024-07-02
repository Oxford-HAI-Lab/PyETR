# Development (advanced)

If you wish to develop with the package, and make new releases, please find instructions for use below:

## Step 1: Install prerequisites

Make sure you first have installed. Note there are additional dependencies to simply running the package:

* Python 3.11 or later: [https://python.org/downloads/](https://python.org/downloads/)
* Poetry [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)
* Poetry bump version (installed with `poetry self add poetry-bumpversion`)

## Step 2: Install poetry package

Once you have the above, installing the package to develop with can be done with:

```
poetry install
```

## Step 3: Setup pre-commit hooks

To ensure code quality, per-commit hooks should be activated. This will automatically reformat new lines of code on commit. Install with

```
poetry run pre-commit install
```

# Releasing a new release

## Step 1: Changes to cases

Any changes to the cases file will result in the `case_list.json` file needing to be updated. This file represents all of the views currently present in `cases.py` and `case_list_extra.json`, so needs to be kept in line with these. You can regenerate the file with:
```
poetry run python generate_case_list.py
```

## Step 2: Check the tests

### Fast Mode (processes in around 10 seconds)

You can run the tests in "fast mode". This is recommended as a good "sanity check" if you're working on developing a new feature (as it covers most use cases), but before making a full release it's recommended to run the full set of tests (see slow mode below).

To run the fast tests, simply navigate to the tests folder and run:

```
poetry run pytest
```

### Slow Mode (processes in around 55 seconds)

Before making a release, it's worth checking the slow mode tests - these run all permutations of the cases view against each other, to search for any inconsistencies. It's also worth running these across multiple cores to increase the speed. This can be run with:

```
poetry run pytest --viewops -n <number_of_cores>
```

## Step 3: Bump the version

Finally bump the version with the below command, using either patch, minor or major:

`poetry version patch`

## Step 4: Commit the latest version

Commit up the above changes to master branch.


## Step 5: Build the package

You then need to build the package with poetry using:
```
poetry build
```

## Step 6: Make the release

You can make a new release [here](https://github.com/dreamingspires/PyETR/releases/new)

Be sure to upload the `*.tar.gz` and `*.whl` files found in the ./dist directory.
