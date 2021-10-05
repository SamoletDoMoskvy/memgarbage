import datetime
import time
import pathlib
from moviepy.editor import *

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from models import Video, Group
from settings import VIDEOS_QUANTITY

ENGINE = create_engine('sqlite:///./memegarbage.db')
SESSION = Session(bind=ENGINE)
BASE = declarative_base(bind=ENGINE)


downloads_folder = pathlib.Path.cwd() / "downloads"
generated_folder = pathlib.Path.cwd() / "generatedVideos"

if not generated_folder.exists():
    generated_folder.mkdir()

shum = VideoFileClip(str(downloads_folder.parent / "shum.mp4")).fx(vfx.speedx, 0.2)

while True:
    result = None
    counter = 0

    if downloads_folder.exists():
        for folder in downloads_folder.glob("*"):
            for video_path in folder.glob("*"):
                try:
                    video = VideoFileClip(str(video_path))
                except OSError:
                    continue

                if counter >= VIDEOS_QUANTITY:
                    # в данном случае видео готово и его нужно сохранить
                    result.write_videofile(str(generated_folder / f"{datetime.datetime.now()}.mp4"))
                    result = None
                    continue

                if not result:
                    result = concatenate_videoclips([video, shum], method="compose")
                    counter += 1

                elif result:
                    result = concatenate_videoclips([result, video, shum], method="compose")
                    counter += 1

    else:
        time.sleep(5)


# write_videofile("myHolidays_edited.webm",fps=25)