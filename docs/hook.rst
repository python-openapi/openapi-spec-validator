pre-commit hook
===============

`pre-commit <https://pre-commit.com>`__ is a framework for building and running `git hooks <https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks>`__.

This document describes available pre-commit hook provided by openapi-spec-validator.

Usage
-----

The ``openapi-spec-validator`` hook calls the openapi-spec-validator command to make sure the specification does not get committed in a broken state. For more information see the :doc:`cli`.

A full .pre-commit-config.yaml example you can use in your repository:

.. code-block:: yaml

   repos:
   -   repo: https://github.com/python-openapi/openapi-spec-validator
       rev: 0.8.0b3 # The version to use or 'master' for latest
       hooks:
       -   id: openapi-spec-validator

For more information on how to use pre-commit please see the official `documentation <https://pre-commit.com>`__.
