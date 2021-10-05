import setup
import download
import os


def command(command):
    os.system(command)


command('clear')
try:
    print('Telegram User:\n     ' + download.client.get_me().first_name + ' ' + download.client.get_me().last_name)
except Exception as ex:
    print('Telegram User:\n     ' + download.client.get_me().first_name)

setup.add_group()
print('Downloading:')
command('sleep 1.5')
download.get_video()
