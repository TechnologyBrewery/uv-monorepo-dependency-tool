# %%
import subprocess
import tempfile
import shutil
from pathlib import Path
import click
import toml

MIXED = "mixed"
EXACT = "exact"


def get_pyproject_path():
    current_working_directory = Path.cwd()
    pyproject_toml_filepath = current_working_directory / "pyproject.toml"

    if pyproject_toml_filepath.exists():
        return pyproject_toml_filepath
    else:
        raise RuntimeError("pyproject.toml path not found.")


def load_pyproject_toml(pyproject_path):
    """Loads a pyproject.toml file."""
    with pyproject_path.open("r", encoding="utf-8") as f:
        return toml.load(f)


def write_pyproject_toml(pyproject_path, data):
    """Writes a pyproject.toml file."""
    with pyproject_path.open("w", encoding="utf-8") as f:
        toml.dump(data, f)


def get_project_version(pyproject_path):
    """Extracts version from a given pyproject.toml file."""
    data = load_pyproject_toml(pyproject_path)
    return data["project"]["version"]


def get_editable_dependencies(data):
    try:
        return data["tool"]["uv"]["sources"]
    except KeyError:
        return None


def get_dependencies(data):
    try:
        return data["project"]["dependencies"]
    except KeyError:
        return None


def remove_empty_editable_dependency_table(data, editable_dependencies_to_delete):
    for dep in editable_dependencies_to_delete:
        del data["tool"]["uv"]["sources"][dep]

    if not data["tool"]["uv"]["sources"]:
        del data["tool"]["uv"]["sources"]


def create_temporary_build_env(package_root, version_pinning_strategy):
    """Creates a temporary directory for a clean build environment."""
    temp_dir = Path(tempfile.mkdtemp())
    click.echo(f"Creating temporary build environment at {temp_dir}")

    # Copy consumer to temp_dir
    package_root_temp = temp_dir / package_root.name
    shutil.copytree(
        package_root,
        package_root_temp,
        ignore=shutil.ignore_patterns(".venv", "dist", "uv.lock"),
    )

    # Read dependencies from the original pyproject.toml
    temp_pyproject_path = package_root_temp / "pyproject.toml"
    data = load_pyproject_toml(temp_pyproject_path)

    editable_dependencies = get_editable_dependencies(data)
    dependencies = get_dependencies(data)
    editable_dependencies_to_delete = []

    for dep_name, dep_value in editable_dependencies.items():
        if dep_name in dependencies:
            editable_dependencies_to_delete.append(dep_name)
            if isinstance(dep_value, dict) and dep_value.get("path"):
                dep_path = Path(dep_value["path"])
                dep_pyproject = dep_path / "pyproject.toml"

                if dep_pyproject.exists():
                    fixed_version = get_project_version(dep_pyproject)
                    dep_name_index = dependencies.index(dep_name)

                    if version_pinning_strategy == EXACT:
                        dependencies[dep_name_index] = f"{dep_name}=={fixed_version}"
                        click.echo(
                            f"Pinning {dep_name} version -> {dep_name}=={fixed_version}"
                        )
                    elif version_pinning_strategy == MIXED:
                        dependencies[dep_name_index] = f"{dep_name}>={fixed_version}"
                        click.echo(
                            f"Pinning {dep_name} version -> {dep_name}>={fixed_version}"
                        )

    if editable_dependencies_to_delete:
        remove_empty_editable_dependency_table(data, editable_dependencies_to_delete)

    # Write the modified pyproject.toml to the temporary directory
    write_pyproject_toml(temp_pyproject_path, data)

    return package_root_temp


def hasEditableDependency(pyproject_path):
    data = load_pyproject_toml(pyproject_path)
    if get_editable_dependencies(data):
        return True
    else:
        return False


@click.command()
@click.option(
    '--version-pinning-strategy',
    default='mixed',
    show_default=True,
    help='Strategy to use for version pinning.',
)
def build_rewrite_path_deps(version_pinning_strategy: str):
    click.echo("version-pinning-strategy is {} ...".format(version_pinning_strategy))

    pyproject_path = get_pyproject_path()
    package_root = pyproject_path.parent

    if hasEditableDependency(pyproject_path):
        """Creates a temporary environment with pinned dependency versions and builds the package."""

        package_root_temp = create_temporary_build_env(
            package_root, version_pinning_strategy
        )

        subprocess.run(["uv", "build"], cwd=package_root_temp, check=True)

        shutil.copytree(
            package_root_temp / "dist", package_root / "dist", dirs_exist_ok=True
        )

        shutil.rmtree(package_root_temp)

    else:
        subprocess.run(["uv", "build"], cwd=package_root, check=True)


@click.group()
def cli():
    """CLI tool for managing monorepo builds in uv projects."""
    pass


cli.add_command(build_rewrite_path_deps)

if __name__ == "__main__":
    cli()
