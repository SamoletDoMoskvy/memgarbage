from django_cron import CronJobBase, Schedule
from django.conf import settings
from download.models import Group, Download, Video
from telethon.sync import TelegramClient, events
import warnings
import re

# TODO Заменить обращения к БД, которые реализованы через mysqlalchemy ORM на обращения, реализованные на Django ORM


# Импорт переменных для работы механизмов скрипта из settings.py
MAX_DURATION, MESSAGES_PER_CYCLE = settings.MAX_DURATION, settings.MESSAGES_PER_CYCLE
API_ID, API_HASH = settings.API_ID, settings.API_HASH
# TODO Переместить инициализацию клиента
client = TelegramClient('session_name', API_ID, API_HASH)
client.start()


def get_group():
    file = open('/home/sdm/Scripts/Python/Django/Memgarbage/bullshitlist.txt', 'r')
    group_list = []
    for row in file:
        group_list.append(re.sub(r'[!:$]+\s?', '', row).strip())
    return group_list


def add_group(group_list=get_group()):
    output = 'Updated:\n'
    c = 1
    for groups in group_list:
        try:
            last_msg = client.get_messages(groups, limit=1)
        except Exception as ex:
            warnings.warn(f'The {groups} does not exists!')
            continue

        group = Group(
            name=groups
        )
        group.save()
        output += str(c) + ') ' + groups + '\n'
        c += 1
    if c == 1:
        output = 'DB is ready'
        print(output)
    else:
        print(output)


def is_exists(required):
    return

#
# def get_groups():
#     group = db.SESSION.query(db.Group).all()
#     groups = []
#     for name in group:
#         groups.append(name.name)
#
#     return groups
#
#
# def get_video(groups=get_groups()):
#     for group in groups:
#         messages = client.get_messages(group, limit=MESSAGES_PER_CYCLE)
#         for message in messages:
#             if message.media is not None:
#                 try:
#                     message.media.document.id
#                     duration = message.file.duration
#                     if duration <= MAX_DURATION:
#                         document_id = message.media.document.id
#                         check = is_exists(document_id)
#                         if not check:
#                             video = db.Video(
#                                 document_id=document_id,
#                                 group=group
#                             )
#                             print('     ' + group + ' ' + str(document_id))
#                             db.SESSION.add(video)
#                             db.SESSION.commit()
#                             path = './downloads/{}/{}'.format(group, document_id)
#                             client.download_media(message=message, file=path)
#                         else:
#                             continue
#                 except:
#                     continue

# TODO: Запилить функционал запланированного запуска cron'ов

#
# class DownloadCronJob(CronJobBase):
#     RUN_EVERY_MINS = 60  # every 1 minutes
#     RETRY_AFTER_FAILURE_MINS = 1
#
#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'download.download_cron_job'  # a unique code
#
#     def do(self):
#         print('ИдИнАхУй')


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1
    MIN_NUM_FAILURES = 3
    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'download.MyCronJob'

    def do(self):
        print("Cron running!")