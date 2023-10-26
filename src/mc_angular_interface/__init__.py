from pathlib import Path
from importlib.resources import files

templates_dir = files("mc_angular_service") / "resources" / "template"

from model_codegen.models import DataModel, from_json
from model_codegen.utils.stringmanipulation import (
    to_camel_case,
    to_kebab_case,
    to_pascal_case
)


def generate(plugin_args):
    print(plugin_args)
    if len(plugin_args) != 2:
        raise ValueError("angular-service generate subcommand expects the following positional arguments `input`, `output_dir`.")
    input_path, output_path = plugin_args
    parent = Path(output_path)
    if parent.exists() and not parent.is_dir():
        raise ValueError(f"path '{parent}' is not a directory")
    

    input_model_path = Path(input_path)
    json_data = input_model_path.read_text()

    model: DataModel = from_json(json_data)

    for entity in model.entities:
        wd = create_directory(entity, parent)
        generate_interface(entity, wd)

def create_directory(entity, parent: Path):
    folder: Path = parent / entity.name
    folder.mkdir(exist_ok=True, parents=True)
    return folder


def generate_interface(entity, wd: Path):
    entity_name = entity.name
    attributes = entity.attributes
    file_name = f"{to_pascal_case(entity_name)}.ts"
    interface_text = build_interface_text(entity_name, attributes)
    (wd /  file_name).write_text(interface_text)


def build_interface_text(entity_name, attributes):
    text = f"""export interface {to_pascal_case(entity_name)} {{
"""
    for attribute in attributes:
        text += f"""  {attribute.name}{"" if attribute.required else "?"}: {attribute.type};
"""
    text += "}"
    return text