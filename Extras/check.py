import requests
import webbrowser
import os
import sys

def get_remote_file_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        response.raise_for_status()

def get_local_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def compare_files(local_file_path, remote_file_url):
    local_content = get_local_file_content(local_file_path)
    remote_content = get_remote_file_content(remote_file_url)

    if local_content != remote_content:
        print("open site update")
        webbrowser.open('https://github.com/hai1723s/discord-message-spammer')
        os.system("pause")
        sys.exit()
    else:
        print("\n")

local_file_path = './Extras/hash'
remote_file_url = 'https://raw.githubusercontent.com/werearecat/normal-obf/main/Extras/hash'

compare_files(local_file_path, remote_file_url)
