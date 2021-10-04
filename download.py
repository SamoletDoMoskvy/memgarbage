from telethon.sync import TelegramClient, events


import models as db


# API & SESSION#
api_id =
api_hash = ''

client = TelegramClient('session_name', api_id, api_hash)
client.start()

print(client.get_me().first_name + ' ' + client.get_me().last_name)


def exists(required):
    return db.SESSION.query(db.exists().where(db.Video.document_id == required)).scalar()


def get_groups():
    group = db.SESSION.query(db.Group).all()
    groups = []
    for name in group:
        groups.append(name.name)

    return groups


def get_video(groups=get_groups()):
    output = ''
    group_c = 1
    for group in groups:
        messages = client.get_messages(group, limit=1)
        message_c = 1
        for message in messages:
            if message.media is not None:
                try:
                    message.media.document.id
                    duration = message.file.duration
                    if duration <= 60:
                        document_id = message.media.document.id(path="downloads")
                        output += group + ' ' + str(document_id)+'\n'
                        check = exists(document_id)
                        if not check:
                            video = db.Video(
                                document_id=document_id,
                                group=group
                            )
                            db.SESSION.add(video)
                            db.SESSION.commit()
                            #client.download_media(message=message)

                            message_c += 1
                        else:
                            continue
                    group_c += 1
                except:
                    continue
            print(output)
    if group_c == 1:
        print('There is nothing to download')
