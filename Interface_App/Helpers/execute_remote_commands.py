import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SSHManager import SSHManager

username = ""
password = ""

def create_remote_directory(dir_name:str, username:str, password:str, server="sndhw3.inp.nsk.su", port=22):
    '''
        Creates a directory on the remote server for a specified user if it doesn't already exist.

        Parameters
        - `dir_name`: The name of the directory to create on the remote server.
        - `username`: The SSH username for connecting to the remote server.
        - `password`: The original, non-encrypted SSH password to authenticate with the server. Before using this function, ensure the password has been decoded to its original form.
        - `server`: The remote server address, default is `"sndhw3.inp.nsk.su"`.
        - `port`: The port for SSH connection, default is `22`.

        Returns
        - `0` if the directory already exists.
        - `-1` if there is an error in creating the directory or if any part of the command fails.

        Note
        This function uses the `SSHManager` class to manage SSH connections and execute commands on the remote server. It checks if the specified directory exists and creates it if not. It handles connection and disconnection automatically.
    '''

    # Initialize and use the SSHManager
    ssh_manager = SSHManager(server, port, username, password)

    try:
        ssh_manager.connect()
        # Example: Run a command
        check_dir_command = "test -d \"/online/users2/" + username + "/" + dir_name + "&& echo \"yes\" || echo \"no\""
        command = ""
        stdout, stderr = ssh_manager.run_command(check_dir_command)
        if "no" in stdout:
            create_dir_command = "mkdir \"/online/users2/" + username + "/" + dir_name
            stdout, stderr = ssh_manager.run_command(create_dir_command)
            if stderr:
                return -1
            else:
                return 0
        if "yes" in stdout:
            return 0
        else:
            return -1

    finally:
        ssh_manager.close()


