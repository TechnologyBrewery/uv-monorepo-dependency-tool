# uv-monorepo-dependency-tool

[![PyPI](https://img.shields.io/pypi/v/uv-monorepo-dependency-tool?logo=python&logoColor=gold)](https://pypi.org/project/uv-monorepo-dependency-tool/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uv-monorepo-dependency-tool?logo=python&logoColor=gold)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/uv-monorepo-dependency-tool?logo=python&logoColor=gold)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/uv-monorepo-dependency-tool?color=blue&label=Installs&logo=pypi&logoColor=gold)](https://pypi.org/project/uv-monorepo-dependency-tool/)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/mit)
[![Build (github)](https://github.com/TechnologyBrewery/uv-monorepo-dependency-tool/actions/workflows/maven.yaml/badge.svg)](https://github.com/TechnologyBrewery/uv-monorepo-dependency-tool/actions/workflows/maven.yaml)

Inspired by the [poetry-monorepo-dependency-plugin](https://github.com/TechnologyBrewery/poetry-monorepo-dependency-plugin), this
[uv](https://docs.astral.sh/uv/) geared tool facilitates the usage of more complex monorepo project structures by pinning version dependencies when
building archives with local path dependencies to other uv projects within the same monorepo.

## Installation

```
uv tool install rewrite-path-dependencies
```

## Usage

During archive building, this tool will rewrite [path dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/#editable-dependencies)
to other uv projects using the corresponding pinned version dependency extracted from the referenced project's `pyproject.toml`.
By referencing pinned version dependencies in published archive files, package consumers may more easily depend on
and install packages that are built within complex monorepos, without needing to replicate the exact folder structure utilized within
the monorepo for that project's dependencies.

For example, assume that `project-a` and `project-a-consumer` are uv projects that exist within the same monorepo and use the following `pyproject.toml`
configurations.

`project-a/pyproject.toml`:
```toml
[project]
name = "project-a"
version = "1.2.3"
```

`project-a-consumer/pyproject.toml`:
```toml
[project]
name = "project-a-consumer"
version = "1.0.0.dev"
dependencies = ["project-a"]

[tool.uv.sources]
project-a = { path = "../project-a", editable = true }
```
When generating `wheel` or `sdist` archives for the `project-a-consumer` project through `rewrite-path-dependencies build`, the corresponding `package-a-consumer` source distribution will be constructed as if its dependency on the
`project-a` project were declared as `project-a = "1.2.3"`.  As a result, package metadata in archives for `project-a-consumer` will shift from
`Requires-Dist: project-a` to `Requires-Dist: project-a==1.2.3`.

### Command line mode

To run this tool via the command line, within the desired package directory run `uv tool run rewrite-path-dependencies build`.

## Licence

`uv-monorepo-dependency-tool` is available under the [MIT licence][mit_licence].

[uv]: https://docs.astral.sh/uv/
[uv build]: https://docs.astral.sh/uv/reference/cli/#uv-build
[mit_licence]: http://dan.mit-license.org/