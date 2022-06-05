import os
import yaml


class Context:
    config_dir = "/.ttldocker/"
    config_file = "config.yaml"

    configs = None

    def __init__(self):
        self.load_config()

    """
        获取配置项
    """

    def get_config(self, domain, key, default_value=None):
        value = self.configs[domain][key];
        if value is None or value == 'None':
            return default_value
        return value

    def load_config(self):
        config_dir = os.environ['HOME'] + self.config_dir
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        if not os.path.exists(self.get_config_path()):
            # TODO: 创建模板文件
            pass

        with open(self.get_config_path(), 'r') as f:
            self.configs = yaml.safe_load(f.read())

    def get_config_path(self):
        return os.environ['HOME'] + self.config_dir + self.config_file


if __name__ == '__main__':
    Context()
