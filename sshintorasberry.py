import time
import paramiko
import string
from config import *


hostname = '192.168.137.121'
port = 22
username = 'pi'
password = 'parola123'
name_user ='nedefinit'

def start_sensors(name_user):
    paramiko.util.log_to_file('paramiko.log')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port, username, password)
    client.exec_command('python Desktop/main/main.py '+ name_user)
    time.sleep(2)
    client.close()

