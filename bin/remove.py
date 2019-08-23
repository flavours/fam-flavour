#!/usr/bin/env python3


from pathlib import Path

import click

import libflavour
from strictyaml import load


def log(string):
    click.echo(f"fam-flavour: {string}")


def remove_requirement(flavour_package_name):
    with Path("app.flavour").open("r") as f:
        yml = f.read()

        yaml_data = load(yml, libflavour.schema.schema_project)

        if flavour_package_name in yaml_data["addons"]:
            log("deleting")
            del yaml_data["addons"][flavour_package_name]
            log("can not add to app.flavour, addon entry already exists")
        else:
            log("could not find entry")

    with Path("app.flavour").open("w") as f:
        f.write(yaml_data.as_yaml())


@click.command()
def add():
    yaml = click.get_text_stream("stdin").read()
    yaml_data = load(yaml, libflavour.schema.schema_addon)
    remove_requirement(yaml_data["meta"]["name"])


if __name__ == "__main__":
    add()
