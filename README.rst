========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/record_converter/badge/?style=flat
    :target: https://record_converter.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/OlivettaDataGarden/record_converter/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/OlivettaDataGarden/record_converter/actions

.. |codecov| image:: https://codecov.io/gh/OlivettaDataGarden/record_converter/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/OlivettaDataGarden/record_converter

.. |version| image:: https://img.shields.io/pypi/v/record-converter.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/record-converter

.. |wheel| image:: https://img.shields.io/pypi/wheel/record-converter.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/record-converter

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/record-converter.svg
    :alt: Supported versions
    :target: https://pypi.org/project/record-converter

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/record-converter.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/record-converter

.. |commits-since| image:: https://img.shields.io/github/commits-since/OlivettaDataGarden/record_converter/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/OlivettaDataGarden/record_converter/compare/v0.0.0...main



.. end-badges

A YAML based dict converter

* Free software: MIT license

Installation
============

::

    pip install record-converter

You can also install the in-development version with::

    pip install https://github.com/OlivettaDataGarden/record_converter/archive/main.zip


Documentation
=============


https://record_converter.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
