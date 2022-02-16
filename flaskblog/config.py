import json
from pathlib import Path
import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", 
                    help="The configuration to use, 'DEFAULT is equivalent to 'DEBUG'.",
                    choices=["debug"],
                    dest="config",
                    type=str,
                    default="debug"
                    )

args = parser.parse_args()

def get_config():
    """Return the config file."""
    return str(Path(__file__).parents[1] / "flaskblog_configs" / f"{args.config}.json")