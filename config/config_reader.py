import yaml
import os


class ConfigReader:
    _config = None
    _env = None

    def __init__(self):
        if ConfigReader._config is None:
            config_path=os.path.join(os.path.dirname(__file__),"config.yaml")

            with open(config_path, "r") as full:
                all_config = yaml.safe_load(full)

            ConfigReader._env = all_config.get("environment", "dev")

            ConfigReader._config = all_config.get(ConfigReader._env, {})

        self.config = ConfigReader._config
        self.env = ConfigReader._env

    def get_env(self):
        return self.env

    def get_base_url(self):
        return self.config.get("base_url")

    def get_api_base_url(self):
        return self.config.get("api_base_url")

    def get_username(self):
        return self.config.get("username")

    def get_password(self):
        return self.config.get("password")

    def get_browser(self):
        return self.config.get("browsers", "chrome")

    def is_headless(self):
        return self.config.get("headless", False)


    def get_implicit_wait(self):
        return self.config.get("implicit_wait", 10)

    def get_explicit_wait(self):
        return self.config.get("explicit_wait", 20)



