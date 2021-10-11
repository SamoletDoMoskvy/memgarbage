from django_cron import CronJobBase, Schedule
from django.conf import settings
from video_downloader.models import Group, Video
from telethon.sync import TelegramClient, events
import time
import warnings
import re

# TODO Переместить инициализацию клиента
# Импорт переменных для работы механизмов скрипта из settings.py
MAX_DURATION, MESSAGES_PER_CYCLE = settings.MAX_DURATION, settings.MESSAGES_PER_CYCLE
API_ID, API_HASH = settings.API_ID, settings.API_HASH
client = TelegramClient('session_name', API_ID, API_HASH)
client.start()


def get_group():
    file = open('/home/sdm/Scripts/Python/Django/Memgarbage/bullshitlist.txt', 'r')
    group_list = []
    for row in file:
        group_list.append(re.sub(r'[!:$]+\s?', '', row).strip())
    return group_list


def add_group(group_list=get_group()):
    output = '  Updated:\n'
    c = 1
    for groups in group_list:
        try:
            last_msg = client.get_messages(groups, limit=1)
        except Exception as ex:
            warnings.warn(f"The {groups} does not exists!")
            continue
        if not bool(len(Group.objects.filter(name=groups))):
            group = Group(
                name=groups
            )
            group.save()
        output += '     '+str(c) + ') ' + groups + '\n'
        c += 1
    if c == 1:
        output = 'DB is ready'
        print(output)
    else:
        print(output)


def is_exists(required):
    return bool(len(Video.objects.filter(document_id=required)))


def get_groups():
    group = [group.name for group in Group.objects.all()]
    return group


def get_video(groups=get_groups()):
    for group in groups:
        messages = client.get_messages(group, limit=MESSAGES_PER_CYCLE)
        for message in messages:
            if message.media is not None:
                try:
                    message.media.document.id
                    duration = message.file.duration
                    if duration <= MAX_DURATION:
                        document_id = message.media.document.id
                        is_exists(document_id)
                        check = is_exists(document_id)
                        if not check:
                            download = Video(
                                document_id=document_id,
                                group=Group.objects.get(name=group),
                            )
                            print('     ' + str(group) + ' ' + str(document_id))
                            download.save()
                            path = './downloads/{}/{}'.format(group, document_id)
                            client.download_media(message=message, file=path)
                        else:
                            continue
                except:
                    continue


class CronDownloader(CronJobBase):
    RUN_EVERY_MINS = 1
    MIN_NUM_FAILURES = 3
    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'video_downloader.CronDownloader'

    def do(self):
        print(f"CronDownloader started at {time.strftime('%D %H:%M:%S')}\n")
        add_group()
        print(' Downloading:')
        get_video()
        print(f"\nCronDownloader finished at {time.strftime('%D %H:%M:%S')}")
