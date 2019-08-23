#!/usr/bin/env python3


import hashlib
import os
from collections import OrderedDict
from pathlib import Path

import click

import libflavour
from strictyaml import as_document


def log(string):
    click.echo(f"fam-flavour: {string}")


def save_yaml(yaml_as_string):
    base_folder = Path(".flavour") / "addons"
    base_folder.mkdir(parents=True, exist_ok=True)

    m = hashlib.sha256()
    m.update(yaml_as_string.encode("utf-8"))
    the_hash = str(m.hexdigest())

    hash_file = base_folder / the_hash
    with hash_file.open("w") as f:
        f.write(yaml_as_string)

    return the_hash


def add_requirement(flavour_package_name, platform_fam, version, yaml_hash):
    flavour_file = "app.flavour"
    with Path(flavour_file).open("r") as f:
        yml = f.read()
        yaml_data = libflavour.Application(yml)._data

        if (
            "addons" in yaml_data
            and flavour_package_name in yaml_data["addons"]
        ):
            log("can not add to configuration, addon entry already exists")
        else:
            log(f"adding new {flavour_package_name}")
            yaml_data["addons"][
                f"{flavour_package_name}:{version}"
            ] = as_document(
                OrderedDict([("manager", platform_fam), ("hash", yaml_hash)])
            )
    with Path(flavour_file).open("w") as f:
        f.write(yaml_data.as_yaml())


@click.command()
def add():
    yaml = click.get_text_stream("stdin").read()
    yaml_data = libflavour.Addon(yaml).data
    yaml_hash = save_yaml(yaml)
    add_requirement(
        flavour_package_name=yaml_data["meta"]["name"],
        platform_fam=os.environ["FAM_IDENTIFIER"],
        version=str(yaml_data["meta"]["version"]),
        yaml_hash=yaml_hash,
    )


if __name__ == "__main__":
    add()
