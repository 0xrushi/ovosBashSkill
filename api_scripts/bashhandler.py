import paramiko
# ANSI escape sequence for red color
red_color = "\033[31m"
# ANSI escape sequence to reset color to default
reset_color = "\033[0m"

class SSHExecutor:
    profiles = {
        'ubuntu': {'hostname': '192.168.4.85', 'username': 'ubuntu', 'password': 'orangepi'},
        'doraemon': {'hostname': '192.168.4.44', 'username': 'doraemon', 'password': 'toor'}
    }

    def __init__(self, profile_key):
        self.set_profile(profile_key)
        self.client = None

    def set_profile(self, profile_key):
        profile = self.profiles.get(profile_key)
        if profile:
            self.hostname = profile['hostname']
            self.username = profile['username']
            self.password = profile['password']
        else:
            raise ValueError(f"Profile '{profile_key}' does not exist.")

    def get_profile(self):
        profile = {
            'hostname': self.hostname,
            'username': self.username,
            'password': self.password
        }
        return profile['hostname']

    def connect(self):
        # Create an SSH client
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the server
        self.client.connect(self.hostname, username=self.username, password=self.password)

    def execute_command(self, command):
        # Execute the command
        _, stdout, _ = self.client.exec_command(command)

        # Read the command output
        output = stdout.read().decode('utf-8')

        return output

    def close(self):
        # Close the SSH session
        self.client.close()

    def run_commands(self, input_text = 'show me currently running pods'):
        # Execute multiple commands
        commandtext = f'cat ~/deleteme.txt | /home/ubuntu/.local/bin/sgpt --shell "{input_text}"'
        commands = [commandtext]
        for command in commands:
            output = self.execute_command(command)
            ch = input(f"Should I execute \n{red_color}{output}{reset_color}? (y/n)")
            if ch.lower() == 'y':
                output = self.execute_command(output)
                print(output)
                ch = input(f"Should I execute \n{red_color}{output}{reset_color}? (y/n)")

# if __name__ == '__main__':

