from toga.paths import PlatformDirsPaths


class Paths(PlatformDirsPaths):
    def get_config_path(self):
        return super().get_config_path() / "Config"

    def get_data_path(self):
        return super().get_config_path() / "Data"
