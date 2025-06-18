# uv-monorepo-dependency-tool

[![PyPI](https://img.shields.io/pypi/v/uv-monorepo-dependency-tool?logo=python&logoColor=gold)](https://pypi.org/project/uv-monorepo-dependency-tool/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uv-monorepo-dependency-tool?logo=python&logoColor=gold)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/uv-monorepo-dependency-tool?logo=python&logoColor=gold)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/uv-monorepo-dependency-tool?color=blue&label=Installs&logo=pypi&logoColor=gold)](https://pypi.org/project/uv-monorepo-dependency-tool/)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/mit)
[![Build uv-monorepo-dependency-tool](https://github.com/TechnologyBrewery/uv-monorepo-dependency-tool/actions/workflows/build.yaml/badge.svg)](https://github.com/TechnologyBrewery/uv-monorepo-dependency-tool/actions/workflows/build.yaml)

## uv-monorepo-dependency-tool

`uv-monorepo-dependency-tool` is a tool designed to help manage dependencies within a Python
monorepo structure, particularly when using `uv` as the package manager. It simplifies the process
of identifying, updating, and synchronizing dependencies across various projects within the
monorepo.

## Features

- **Automated Rewrite of Path Dependencies**: Converts editable path dependencies into pinned version dependencies during archive generation.
- **Improved Package Metadata**: Adjusts dependency metadata in generated archives to use pinned versions, ensuring better compatibility for consumers of the package.
- **Monorepo Support**: Designed specifically for managing dependencies across complex UV-based monorepos.
- **CLI Support**: Run commands directly from the terminal for seamless integration with your development workflow.

For more detailed information about the tool, its features, and usage instructions, please refer
to the dedicated [README.md](uv-monorepo-dependency-tool/README.md).

This project was inspired by our sister effort, the [PoetryMonorepoDependencyPlugin](https://github.com/TechnologyBrewery/poetry-monorepo-dependency-plugin).

## Examples

The `examples` folder contains sample projects demonstrating various use cases and configurations of the `uv-monorepo-dependency-tool`.

*   **[project-a](examples/project-a/README.md)**: Using the uv-monorepo-dependency-tool for a single reusable module in a monorepo project.
*   **[project-a-consumer](examples/project-a-consumer/README.md)**: A monorepo project that consumes the module from `project-a`.