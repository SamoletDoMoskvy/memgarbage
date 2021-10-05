from sqlalchemy import exists
from telethon.sync import TelegramClient, events
import models as db
import os, os.path

# API & SESSION#
from settings import MAX_DURATION, MESSAGES_PER_CYCLE

api_id = 8485098
api_hash = 'cc19e8236773b9c6178ca92ae5310cc9'

client = TelegramClient('session_name', api_id, api_hash)
client.start()


def is_exists(required):
    return db.SESSION.query(exists().where(db.Video.document_id == required)).scalar()


def get_groups():
    group = db.SESSION.query(db.Group).all()
    groups = []
    for name in group:
        groups.append(name.name)

    return groups


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
                        check = is_exists(document_id)
                        if not check:
                            video = db.Video(
                                document_id=document_id,
                                group=group
                            )
                            print('     ' + group + ' ' + str(document_id))
                            db.SESSION.add(video)
                            db.SESSION.commit()
                            path = './downloads/{}/{}'.format(group, document_id)
                            client.download_media(message=message, file=path)
                        else:
                            continue
                except:
                    continue
