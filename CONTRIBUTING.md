# Contributing 

## Table of Contents
 * [Introduction](#introduction)
 * [Getting started](#getting-started)
 * [How to report a bug](#How-to-report-a-bug)
 * [How to suggest a new feature](#How-to-suggest-a-new-feature)
 * [Code review process](#Code-review-process)

## Introduction

First off, thank you for considering contributing to Scout Suite, you're awesome! 🎉

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

## Getting started

So you want to contribute some code, that's great! This project follows the [GitHub Workflow](https://guides.github.com/introduction/flow/). 

### Setting up a local environment

Python 3.11 is the verified/recommended local dev version (matches the CI target's language level; CI itself runs on `ubuntu-latest`).

```
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r dev-requirements.txt
```

**Windows only:** `dev-requirements.txt` pulls in `pyreadline 2.1` transitively (via `humanfriendly`, required by `azure-cli-core==2.12.0`, which pins `humanfriendly<9.0`). `pyreadline 2.1` is incompatible with Python 3.10+ (`collections.Callable` was removed) and will crash `pytest` on startup with `AttributeError: module 'collections' has no attribute 'Callable'`. This only affects local Windows dev — `humanfriendly` already restricts `pyreadline` to `sys_platform == "win32"` upstream, so it is never installed on CI. If you hit this, swap it for the maintained fork:

```
pip uninstall -y pyreadline
pip install pyreadline3
```

1. If it's a complex issue, please describe how you plan on going about addressing it on the issue thread.
2. Assign yourself to the issue
3. Create a branch using the following naming convention:
    * If it's a feature: `feature/issuenumber-descriptive-name` 
    * If it's a bug fix: `bugfix/issuenumber-descriptive-name` 
    * If it's a hot fix: `hotfix/issuenumber-descriptive-name` 
4. Implement your solution and the associated tests
5. Make sure your code follows the [PEP8 guidelines](https://www.python.org/dev/peps/pep-0008/)
6. [Create a pull request](https://help.github.com/articles/creating-a-pull-request/) against `develop`
7. Wait for people to review it
8. Address the comments people left on your pull request
9. Go back to 7. and repeat until your PR is 💯 
10. Wait for someone from the team to merge your PR

## How to report a bug

When filing an issue, make sure to answer these five questions:

 1. What version of Python are you using?
 2. What operating system and processor architecture are you using?
 3. What did you do?
 4. What did you expect to see?
 5. What did you see instead?

## How to suggest a new feature

If you find yourself wishing for a feature that doesn't exist in Scout Suite, you are probably not alone. There are bound to be others out there with similar needs. Many of the features that Scout Suite has today have been added because our users saw the need. Open an issue on our issues list on GitHub which describes the feature you would like to see, why you need it, and how it should work.

## Code review process

Pull requests are regularly reviewed by the core team. We require a minimum of two reviewers before allowing to merge. 
