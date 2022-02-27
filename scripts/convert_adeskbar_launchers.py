import configparser
from pathlib import Path, PurePath

import yaml

config = configparser.ConfigParser()
config.read(PurePath(Path.home(), '.config/adeskbar/default.cfg'))

launchers = []

for section in config.sections():
    if not section.startswith('LAUNCHER'):
        continue

    launchers.append({k: v for k, v in config[section].items()})

print(yaml.dump({"launchers": launchers}))
