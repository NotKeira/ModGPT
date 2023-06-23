import json
import os


class Database:
    def __init__(self):
        self.guilds_file = os.path.join('database', 'guilds.json')
        self.users_file = os.path.join('database', 'users.json')
        self.commands_file = os.path.join('database', 'command_list.json')
        self.blacklisted_file = os.path.join('database', 'blacklisted.json')
        self.reminders_file = os.path.join('database', 'reminders.json')
        self.usage_file = os.path.join('database', 'usage.json')
        self.infractions_file = os.path.join('database', 'infractions.json')
        self.tickets_file = os.path.join('database', 'tickets.json')
        self.ticket_transcripts_file = os.path.join('database', 'transcripts.json')
        self.ensure_file_exists(self.guilds_file)
        self.ensure_file_exists(self.users_file)
        self.ensure_file_exists(self.commands_file)
        self.ensure_file_exists(self.blacklisted_file)
        self.ensure_file_exists(self.reminders_file)
        self.ensure_file_exists(self.usage_file)
        self.ensure_file_exists(self.infractions_file)
        self.ensure_file_exists(self.tickets_file)
        self.ensure_file_exists(self.ticket_transcripts_file)

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

    def read_blacklisted_words(self):
        return self.read_data(self.blacklisted_file)

    def add_reminder(self, data):
        existing_data = self.get_reminders()
        existing_data.update(data)
        self.write_data(existing_data, self.reminders_file)

    def delete_reminder(self, identifier):
        data = self.get_reminders()
        if identifier in data:
            del data[identifier]
            self.write_data(data, self.reminders_file)

    def get_reminders(self):
        return self.read_data(self.reminders_file)

    def get_usage(self):
        return self.read_data(self.usage_file)

    def add_usage(self, data):
        self.write_data(data, self.usage_file)

    def delete_usage(self, identifier):
        data = self.get_usage()
        if identifier in data:
            del data[identifier]
            self.write_data(data, self.usage_file)

    def get_guild_value(self, guild_id, key):
        data = self.read_guild_data()
        return self.get_value(data, f'{guild_id}.{key}')

    def set_guild_value(self, guild_id, key, value):
        data = self.read_guild_data()
        self.set_value(data, f'{guild_id}.{key}', value)
        self.write_guild_data(data)

    def delete_guild_value(self, guild_id, key):
        data = self.read_guild_data()
        self.delete_value(data, f'{guild_id}.{key}')
        self.write_guild_data(data)

    def get_infractions(self):
        return self.read_data(self.infractions_file)

    def add_infraction(self, data, identifier):
        existing_data = self.get_infractions()
        option = data[str(identifier)]['type']
        if option not in ['warn', 'mute', 'kick', 'ban', 'report']:
            print("Invalid option")
            return False

        if option == 'warn':
            option = 'warns'
        elif option == 'mute':
            option = 'mutes'
        elif option == 'kick':
            option = 'kicks'
        elif option == 'ban':
            option = 'bans'
        elif option == 'report':
            option = 'reports'

        if option not in existing_data:
            existing_data[option] = {}

        identifier = list(data.keys())[0]  # Get the first (and only) key from the data dictionary
        existing_data[option][identifier] = data[identifier]
        self.write_data(existing_data, self.infractions_file)
        return True

    def delete_infraction(self, option, identifier):
        if option not in ['warns', 'mutes', 'kicks', 'bans']:
            return print("Invalid option")
        if option == 'warn':
            option = 'warns'
        elif option == 'mute':
            option = 'mutes'
        elif option == 'kick':
            option = 'kicks'
        elif option == 'ban':
            option = 'bans'
        elif option == 'report':
            option = 'reports'

        data = self.get_infractions()
        if option in data:
            if identifier in data[option]:
                del data[option][identifier]
                self.write_data(data, self.infractions_file)
                return True

    def get_infraction(self, option, identifier):
        if option not in ['warns', 'mutes', 'kicks', 'bans']:
            return print("Invalid option")
        if option == 'warn':
            option = 'warns'
        elif option == 'mute':
            option = 'mutes'
        elif option == 'kick':
            option = 'kicks'
        elif option == 'ban':
            option = 'bans'
        elif option == 'report':
            option = 'reports'

        data = self.get_infractions()
        if option in data:
            if identifier in data[option]:
                return data[option][identifier]
        return None

    def get_infraction_count(self, option, user_id):
        if option not in ['warns', 'mutes', 'kicks', 'bans']:
            return print("Invalid option")
        if option == 'warn':
            option = 'warns'
        elif option == 'mute':
            option = 'mutes'
        elif option == 'kick':
            option = 'kicks'
        elif option == 'ban':
            option = 'bans'
        elif option == 'report':
            option = 'reports'

        data = self.get_infractions()
        if option in data:
            count = 0
            for identifier in data[option]:
                if data[option][identifier]['user_id'] == user_id:
                    count += 1
            return count
        return 0

    # Tickets

    def get_ticket_data(self):
        return self.read_data(self.tickets_file)

    def add_ticket(self, data, identifier):
        existing_data = self.get_ticket_data()
        if identifier not in existing_data:
            existing_data[identifier] = data
        self.write_data(existing_data, self.tickets_file)

    def delete_ticket(self, identifier):
        data = self.get_ticket_data()
        if identifier in data:
            del data[identifier]
            self.write_data(data, self.tickets_file)

    def get_ticket(self, identifier):
        data = self.get_ticket_data()
        if identifier in data:
            return data[identifier]
        return None

    def edit_ticket(self, identifier, value):
        data = self.get_ticket_data()
        if identifier in data:
            data[identifier] = value
            self.write_data(data, self.tickets_file)

    # Ticket Transcripts

    def get_transcripts(self):
        return self.read_data(self.ticket_transcripts_file)

    def get_transcript(self, identifier):
        data = self.read_data(self.ticket_transcripts_file)
        if identifier in data:
            return data[identifier]
        return None

    def add_transcript(self, data, identifier):
        existing_data = self.read_data(self.ticket_transcripts_file)
        if identifier not in existing_data:
            existing_data[identifier] = data
        self.write_data(existing_data, self.ticket_transcripts_file)

    def delete_transcript(self, identifier):
        data = self.read_data(self.ticket_transcripts_file)
        if identifier in data:
            del data[identifier]
            self.write_data(data, self.ticket_transcripts_file)
