import json


class Config(dict):
    def __init__(self, config_path: str):
        self.config_path = config_path

        # Opens the existing, or creates a new config file if one
        #  didn't already exist
        while True:
            try:
                with open(self.config_path, 'r') as config_file:
                    config_file_content = json.load(config_file)
                    break
            except FileNotFoundError:
                with open(self.config_path, 'w') as config_file:
                    json.dump("{}", config_file)

        # Convert the config file content to a dict if its of the type str
        if isinstance(config_file_content, str):
            config_file_content = json.loads(config_file_content) 

        # Merge the instance dict with the config file's dict 
        for key,value in config_file_content.items():
            self[key] = value



    def __setitem__(self, key, value):
        super().__setitem__(key,value)

    def __getitem__(self, key):
        return super().__getitem__(key)   

    
    def write(self):
        with open(self.config_path, 'w') as config_file:
            json.dump(dict(self), config_file)


if __name__=="__main__":
    settings = Config('test.json')
    
