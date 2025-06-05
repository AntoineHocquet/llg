import json
import os

"""
Tools for loading and saving simulation parameters.
"""


def load_config():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(root, "params.json")
    with open(config_path, "r") as f:
        config = json.load(f)
    return config


def save_config(params):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(root, "params.json")
    with open(config_path, "w") as f:
        json.dump(params, f, indent=4)

