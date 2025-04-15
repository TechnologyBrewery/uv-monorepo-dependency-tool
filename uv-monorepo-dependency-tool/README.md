# uv-monorepo-dependency-tool

[![PyPI](https://img.shields.io/pypi/v/uv-monorepo-dependency-tool?logo=python&logoColor=gold)](https://pypi.org/project/uv-monorepo-dependency-tool/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uv-monorepo-dependency-tool?logo=python&logoColor=gold)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/uv-monorepo-dependency-tool?logo=python&logoColor=gold)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/uv-monorepo-dependency-tool?color=blue&label=Installs&logo=pypi&logoColor=gold)](https://pypi.org/project/uv-monorepo-dependency-tool/)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/mit)
[![Build (github)](https://github.com/TechnologyBrewery/uv-monorepo-dependency-tool/actions/workflows/maven.yaml/badge.svg)](https://github.com/TechnologyBrewery/uv-monorepo-dependency-tool/actions/workflows/maven.yaml)

## Overview

The `uv-monorepo-dependency-tool` is designed to simplify dependency management in monorepos that utilize [path dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/#editable-dependencies). It streamlines the process of building archives by rewriting path dependencies to reference the appropriate pinned version dependencies from the referenced project's `pyproject.toml`.

This helps package consumers avoid replicating complex folder structures within their own projects. Instead, they can directly rely on the pinned version dependencies specified during the archive-building process.

## Features

- **Automated Rewrite of Path Dependencies**: Converts editable path dependencies into pinned version dependencies during archive generation.
- **Improved Package Metadata**: Adjusts dependency metadata in generated archives to use pinned versions, ensuring better compatibility for consumers of the package.
- **Monorepo Support**: Designed specifically for managing dependencies across complex UV-based monorepos.
- **CLI Support**: Run commands directly from the terminal for seamless integration with your development workflow.

## Getting Started

### Installation

To use this tool in your environment, from the root project directory run
```bash
#TODO: update to published package
uv tool install uv-monorepo-dependency-tool/dist/uv_monorepo_dependency_tool-1.0.0.dev0-py3-none-any.whl 
```

### Usage

The `uv-monorepo-dependency-tool` works during the archive-building process. It analyzes `pyproject.toml` files of dependencies in the monorepo and replaces editable path dependencies with the corresponding pinned version dependencies.

For example, assume that `project-a` and `project-a-consumer` are uv projects that exist within the same monorepo and use the following `pyproject.toml`
configurations.

`project-a/pyproject.toml`:
```toml
[project]
name = "project-a"
version = "1.0.0.dev0"
```

`project-a-consumer/pyproject.toml`:
```toml
[project]
name = "project-a-consumer"
version = "1.0.0.dev0"
dependencies = ["project-a"]

[tool.uv.sources]
project-a = { path = "../project-a", editable = true }
```
When generating `wheel` or `sdist` archives for `project-a-consumer`  via `build-rewrite-path-deps`, the corresponding `package-a-consumer` source distribution will be constructed as if its dependency on the
`project-a` project were declared as `project-a = "1.0.0.dev0"`.  As a result, package metadata in archives for `project-a-consumer` will shift from
`Requires-Dist: project-a` to `Requires-Dist: project-a=="1.0.0.dev0"`.

#### Command Line Mode

To execute the tool from the command line, navigate to the desired package directory and run the following command:

```bash
uv tool run uv-monorepo-dependency-tool build-rewrite-path-deps --version-pinning-strategy=mixed     
```

This will generate the updated archive with the rewritten dependencies.

### Configuration

The following cli options are supported :

    * `--version-pinning-strategy` (`string`, default: `mixed`, options: `mixed`, `exact`): Strategy by which path
      dependencies to other Poetry projects will be versioned in generated archives. Given a path dependency to a Poetry project
      with version `1.2.3`, the version of the dependency referenced in the generated archive is `=1.2.3` for `exact`.  `mixed` mode switches versioning strategies based on whether the dependency
      UV project version is an in-flight development version or a release - if a development version (i.e. `1.2.3.dev456`),
      `mixed` can be used to specify the inclusion of subsequent dev releases (i.e. `>=1.2.3.dev`), and
      if a release version (i.e. `1.2.3`), `exact` is applied (i.e. `=1.2.3`).

## Licence

`uv-monorepo-dependency-tool` is available under the [MIT licence][mit_licence].

[uv]: https://docs.astral.sh/uv/
[uv build]: https://docs.astral.sh/uv/reference/cli/#uv-build
[mit_licence]: http://dan.mit-license.org/