import os
import yaml


class Config:
    def __init__(self):
        self.config_path: str = os.getenv('CONFIG_PATH','data/config.yaml')
        with open(self.config_path, 'r') as f:
            config_data = yaml.load(f, Loader=yaml.FullLoader)
        self.data = config_data

    def __getitem__(self, item):
        return self.data[item]

    def get(self,item,defeat):
        self.data.get(item,defeat)