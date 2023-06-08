import json
import os


class CustomDatabase:
    def __init__(self, guilds_file='guilds.json', users_file='users.json'):
        self.guilds_file = os.path.join('database', guilds_file)
        self.users_file = os.path.join('database', users_file)
        self.commands_file = os.path.join('database', 'commands.json')
        self.ensure_file_exists(self.guilds_file)
        self.ensure_file_exists(self.users_file)
        self.ensure_file_exists(self.commands_file)

    @staticmethod
    def ensure_file_exists(file_path):
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write(json.dumps({}))

    @staticmethod
    def read_data(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    @staticmethod
    def write_data(data, file_path):
        with open(file_path, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def get_value(data, key):
        keys = key.split('.')
        for k in keys:
            if k in data:
                data = data[k]
            else:
                return None
        return data

    @staticmethod
    def set_value(data, key, value):
        keys = key.split('.')
        last_key = keys.pop()
        for k in keys:
            if k not in data:
                data[k] = {}
            data = data[k]
        data[last_key] = value

    @staticmethod
    def delete_value(data, key):
        keys = key.split('.')
        last_key = keys.pop()
        for k in keys:
            if k in data:
                data = data[k]
            else:
                return
        if last_key in data:
            del data[last_key]

    def read_guild_data(self):
        return self.read_data(self.guilds_file)

    def write_guild_data(self, data):
        self.write_data(data, self.guilds_file)

    def read_user_data(self):
        return self.read_data(self.users_file)

    def write_user_data(self, data):
        self.write_data(data, self.users_file)

    def read_command_data(self):
        return self.read_data(self.commands_file)
