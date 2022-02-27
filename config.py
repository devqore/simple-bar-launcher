from pathlib import Path

import yaml

# will be used probably to generate config
defaults = {
    "icon_size": 44,
    "hidden_width": 2,
    "hide_timeout_msec": 900,
    "layout_spacing": 5
}


class Config:
    configLocation = Path(Path.home(), '.config/simple-bar-launcher/config.yaml')

    def __init__(self):
        self.config = self.getConfig()

    def getConfig(self):
        if not self.configLocation.is_file():
            self.configLocation.parent.mkdir(parents=True, exist_ok=True)
            raise EnvironmentError(f"Config '{self.configLocation}' doesn't exist. Exiting.")

        with open(self.configLocation, 'r') as file:
            config = yaml.safe_load(file)

        return config

    @property
    def launchers(self):
        launchers = self.config.get('launchers')
        if not launchers:
            raise EnvironmentError(f"Fix launcher section in {self.configLocation}")

        return launchers

    def getFromConfigOrDefault(self, value):
        return self.config.get(value, defaults[value])

    @property
    def hiddenWidth(self):
        return self.getFromConfigOrDefault('hidden_width')

    @property
    def iconSize(self):
        return self.getFromConfigOrDefault('icon_size')

    @property
    def hideTimeoutMsec(self):
        return self.getFromConfigOrDefault('hide_timeout_msec')

    @property
    def layoutSpacing(self):
        return self.getFromConfigOrDefault('layout_spacing')
