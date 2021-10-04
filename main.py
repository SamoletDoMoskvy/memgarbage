import setup
import download
import os


def command(command):
    os.system(command)


command('clear')

setup.add_group()
print('Downloading:')
command('sleep 1.5')
download.get_video()
