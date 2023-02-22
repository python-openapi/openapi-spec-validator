Contributing
============

Firstly, thank you all for taking the time to contribute.

The following section describes how you can contribute to the openapi-spec-validator project on GitHub.

Reporting bugs
--------------

Before you report
^^^^^^^^^^^^^^^^^

* Check whether your issue does not already exist in the `Issue tracker <https://github.com/p1c2u/openapi-spec-validator/issues>`__.
* Make sure it is not a support request or question better suited for `Discussion board <https://github.com/p1c2u/openapi-spec-validator/discussions>`__.

How to submit a report
^^^^^^^^^^^^^^^^^^^^^^

* Include clear title.
* Describe your runtime environment with exact versions you use.
* Describe the exact steps which reproduce the problem, including minimal code snippets.
* Describe the behavior you observed after following the steps, pasting console outputs.
* Describe expected behavior to see and why, including links to documentations.

Code contribution
-----------------

Prerequisites
^^^^^^^^^^^^^

Install `Poetry <https://python-poetry.org>`__ by following the `official installation instructions <https://python-poetry.org/docs/#installation>`__. Optionally (but recommended), configure Poetry to create a virtual environment in a folder named ``.venv`` within the root directory of the project:

.. code-block:: console

   poetry config virtualenvs.in-project true

Setup
^^^^^

To create a development environment and install the runtime and development dependencies, run:

.. code-block:: console

   poetry install

Then enter the virtual environment created by Poetry:

.. code-block:: console

   poetry shell

Static checks
^^^^^^^^^^^^^

The project uses static checks using fantastic `pre-commit <https://pre-commit.com/>`__. Every change is checked on CI and if it does not pass the tests it cannot be accepted. If you want to check locally then run following command to install pre-commit.

To turn on pre-commit checks for commit operations in git, enter:

.. code-block:: console

   pre-commit install

To run all checks on your staged files, enter:

.. code-block:: console

   pre-commit run

To run all checks on all files, enter:

.. code-block:: console

   pre-commit run --all-files

Pre-commit check results are also attached to your PR through integration with Github Action.
