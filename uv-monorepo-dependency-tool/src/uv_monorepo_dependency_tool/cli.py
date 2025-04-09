import subprocess
import tempfile
import shutil
from pathlib import Path
import click
import toml


def find_package_root():
    current_working_directory = Path.cwd()
    pyproject_toml_filepath = current_working_directory / "pyproject.toml"

    if pyproject_toml_filepath.exists():
        return current_working_directory
    else:
        raise RuntimeError("Package root not found.")


def get_version_from_pyproject(pyproject_path):
    """Extracts version from a given pyproject.toml file."""
    with pyproject_path.open("r", encoding="utf-8") as f:
        data = toml.load(f)
        return data["project"]["version"]


def create_temporary_build_env(package_root):
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
    pyproject_path = package_root_temp / "pyproject.toml"
    with pyproject_path.open("r", encoding="utf-8") as f:
        data = toml.load(f)

    editable_dependencies = data["tool"]["uv"]["sources"]
    dependencies = data["project"]["dependencies"]
    editable_dependencies_to_delete = []

    for dep_name, dep_value in editable_dependencies.items():
        if dep_name in dependencies:
            editable_dependencies_to_delete.append(dep_name)
            if isinstance(dep_value, dict) and dep_value.get("path"):
                dep_path = Path(dep_value["path"])
                dep_pyproject = dep_path / "pyproject.toml"

                if dep_pyproject.exists():
                    fixed_version = get_version_from_pyproject(dep_pyproject)
                    dep_name_index = dependencies.index(dep_name)
                    dependencies[dep_name_index] = f"{dep_name}=={fixed_version}"
                    click.echo(
                        f"Pinning {dep_name} version -> {dep_name}=={fixed_version}"
                    )

    if editable_dependencies_to_delete:
        for dep in editable_dependencies_to_delete:
            del data["tool"]["uv"]["sources"][dep]

    if not data["tool"]["uv"]["sources"]:
        del data["tool"]["uv"]["sources"]

    # Write the modified pyproject.toml to the temporary directory
    with pyproject_path.open("w", encoding="utf-8") as f:
        toml.dump(data, f)

    return package_root_temp


@click.command()
def build_rewrite_path_deps():
    """Creates a temporary environment with pinned dependency versions and builds the package."""
    package_root = find_package_root()

    package_root_temp = create_temporary_build_env(package_root)

    click.echo("Building package...")
    subprocess.run(["uv", "build"], cwd=package_root_temp, check=True)

    shutil.copytree(
        package_root_temp / "dist", package_root / "dist", dirs_exist_ok=True
    )

    click.echo(f"Build completed in {package_root_temp}")

    shutil.rmtree(package_root_temp)
    click.echo("Temporary directory removed.")


@click.group()
def cli():
    """CLI tool for managing monorepo builds."""
    pass


cli.add_command(build_rewrite_path_deps)

if __name__ == "__main__":
    cli()
