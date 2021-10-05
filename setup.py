from sqlalchemy import exists
import models as db
import re
from download import client
import warnings


def get_group():
    file = open('bullshitlist.txt', 'r')
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

        if db.SESSION.query(exists().where(db.Group.name == groups)).scalar():
            continue

        else:
            group = db.Group(
                name=groups
            )
            output += str(c) + ') ' + groups + '\n'
            c += 1
        db.SESSION.add(group)
        db.SESSION.commit()
    if c == 1:
        output = 'DB is ready'
        print(output)
    else:
        print(output)
