import os
import yaml


class Context:

    configs = None

    def __init__(self, config_path):
        self.load_config(config_path)

    """
        获取配置项
    """

    def get_root_config(self, key, default_value=None):
        value = self.configs[key]
        if value is None or value == 'None':
            return default_value
        return value

    def get_config(self, domain, key, default_value=None):
        value = self.configs[domain][key]
        if value is None or value == 'None':
            return default_value
        return value

    def load_config(self, config_path):
        if not os.path.exists(config_path):
            print("配置文件不存在")
            exit(1)

        with open(config_path, 'r') as f:
            self.configs = yaml.safe_load(f.read())


if __name__ == '__main__':
    Context()
