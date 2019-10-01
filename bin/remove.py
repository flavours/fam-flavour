#!/usr/bin/env python3


from pathlib import Path

import click

import libflavour
from strictyaml import load


def log(string):
    click.echo(f"fam-flavour: {string}")


def remove_requirement(flavour_package_name, version):
    with Path("app.flavour").open("r") as f:
        yml = f.read()

        yaml_data = load(yml, libflavour.schema.schema_project)
        name_and_version = f"{flavour_package_name}:{version}"
        if name_and_version in yaml_data["addons"]:
            log("deleting")
            p = (
                Path(".flavour")
                / "addons"
                / str(yaml_data["addons"][name_and_version]["hash"])
            )
            p.unlink()
            del yaml_data["addons"][name_and_version]

            log("can not add to app.flavour, addon entry already exists")
        else:
            log("could not find entry")

    with Path("app.flavour").open("w") as f:
        f.write(yaml_data.as_yaml())


@click.command()
def add():
    yaml = click.get_text_stream("stdin").read()
    yaml_data = load(yaml, libflavour.schema.schema_addon)
    remove_requirement(yaml_data["meta"]["name"], yaml_data["meta"]["version"])


if __name__ == "__main__":
    add()
