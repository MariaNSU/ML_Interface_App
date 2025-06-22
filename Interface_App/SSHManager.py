import paramiko
import socket
from time import sleep

class SSHManager:
    def __init__(self, server, port, username, password):
        """Initialize the SSHManager with connection details."""
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.client = None

    def connect(self, timeout=3, fast_fail=True):
        """Establish SSH connection with optimized timeouts and fast failure.

        Args:
            timeout (int): Base timeout in seconds (default 3)
            fast_fail (bool): If True, skip DNS retries on failure

        Returns:
            bool: True if connection succeeded
        """
        # Проверка DNS перед подключением (экономит время при неработающем DNS)
        if fast_fail:
            try:
                socket.getaddrinfo(self.server, self.port, family=socket.AF_INET)
            except socket.gaierror:
                print(f"DNS resolution failed immediately for {self.server}")
                return False

        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


            self.client.connect(
                hostname=self.server,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=timeout,  # Таймаут TCP-соединения
                banner_timeout=timeout / 2,  # Быстрый фейл если сервер не отправляет баннер
                auth_timeout=timeout,  # Таймаут аутентификации
                allow_agent=False,  # Отключаем проверку SSH-агента
                look_for_keys=False  # Отключаем поиск ключей
            )
            print(f"SSH connected to {self.server} in {timeout}s")
            return True

        except Exception as e:
            error_type = type(e).__name__
            print(f"Connection failed [{error_type}]: {str(e)}")
            return False

    def close(self):
        """Close the SSH connection."""
        if self.client:
            self.client.close()
            print("SSH connection closed.")

    def transfer_file(self, local_file, remote_file):
        """Transfer a file to the remote server."""
        if self.client:
            sftp = self.client.open_sftp()
            sftp.put(local_file, remote_file)
            sftp.close()
            print(f"File {local_file} transferred to {remote_file}.")
        else:
            print("No connection established.")

    def retrieve_file(self, remote_file, local_file):
        """Retrieve a file from the remote server to the local computer."""
        if self.client:
            sftp = self.client.open_sftp()
            sftp.get(remote_file, local_file)
            sftp.close()
            print(f"File {remote_file} retrieved to {local_file}.")
        else:
            print("No connection established.")

    def run_command(self, command):
        """Execute a command on the remote server and return its output."""
        if self.client:
            stdin, stdout, stderr = self.client.exec_command(command)
            print(f"Command '{command}' executed.")
            return stdout.read().decode(), stderr.read().decode()
        print("No connection established.")
        return None, None




# Example usage of SSHManager
def example_usage():
    # Connection details
    server = "sndhw3.inp.nsk.su"
    port = 22
    username = ""
    password = ""

    # Initialize and use the SSHManager
    ssh_manager = SSHManager(server, port, username, password)

    try:
        if ssh_manager.connect():
            # Example: Transfer a file
            local_file_path = "ML_APP/TMVAnalysisMy_hd22.C"
            remote_file_path = "/online/users2/petrovam/ML_APP_test/TMVAnalysisMy_hd22.C"
            ssh_manager.transfer_file(local_file_path, remote_file_path)

            # Example: Run a command
            comand0 = "cd /online/users2/petrovam/ML_APP_test/ && source /usr/local/cern/rootsetup.sh 5.18.00"
            stdout, stderr = ssh_manager.run_command(comand0)
            print("Command0 Output:\n", stdout)
            print("Command Error (if any):\n", stderr)

            command = f"root -l -q {remote_file_path}"
            stdout, stderr = ssh_manager.run_command(command)
            print("Command Output:\n", stdout)
            print("Command Error (if any):\n", stderr)

    finally:
        ssh_manager.close()



def is_server_alive(host, port=22, timeout=1):
    """Проверяет доступность порта за 1 секунду"""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

