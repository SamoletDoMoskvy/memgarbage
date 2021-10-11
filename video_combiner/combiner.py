from django_cron import CronJobBase, Schedule
from django.conf import settings
from video_downloader.models import Video
from django.conf import settings
from moviepy.editor import *
import datetime
import pathlib
import time


def comb():
    downloads_folder = pathlib.Path.cwd() / "downloads"
    generated_folder = pathlib.Path.cwd() / "generatedVideos"
    shum = VideoFileClip(str(downloads_folder.parent / "shum.mp4")).fx(vfx.speedx, 4)

    if not generated_folder.exists():
        generated_folder.mkdir()
    while True:
        result = None
        counter = 0

        if downloads_folder.exists():
            for folder in downloads_folder.glob("*"):
                for video_path in folder.glob("*"):
                    # Кидаем в БД метку об использовании видео
                    document_id = video_path.stem
                    if Video.objects.get(document_id=document_id).already_used:
                        continue
                    else:
                        Video.objects.filter(document_id=document_id).update(already_used=True)
                        try:
                            video = VideoFileClip(str(video_path))
                        except OSError:
                            continue

                        if counter + 1 >= settings.VIDEOS_QUANTITY:
                            # в данном случае видео готово и его нужно сохранить
                            result.write_videofile(str(generated_folder / f"{datetime.datetime.now()}.mp4"))
                            result = None
                            counter = 0
                            continue

                        if not result:
                            result = concatenate_videoclips([video, shum], method="compose")
                            counter += 1

                        elif result:
                            result = concatenate_videoclips([result, video, shum], method="compose")
                            counter += 1

        else:
            time.sleep(5)


class CronCombiner(CronJobBase):
    RUN_EVERY_MINS = 1
    MIN_NUM_FAILURES = 3
    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'video_combiner.CronCombiner'

    def do(self):
        print(f"CronCombiner started at {time.strftime('%D %H:%M:%S')}\n")
        comb()
        print(f"\nCronDownloader finished at {time.strftime('%D %H:%M:%S')}")
