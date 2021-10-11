import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from django_cron import CronJobBase, Schedule
from google import auth
from googleapiclient.http import MediaFileUpload
import pathlib
import time

scopes = ["https://www.googleapis.com/auth/youtube.upload"]
file_to_upload = list((pathlib.Path.cwd() / "/home/sdm/Scripts/Python/Django/Memgarbage/generatedVideos").glob("*"))[0]
print(f"uploading file path: {file_to_upload}")


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    # TODO Cron дропается на 27 строчке кода, ничего не возвращает
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    print(flow)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": "test_video",
                "title": "Test video upload."
            },
            "status": {
                "privacyStatus": "private"
            }
        },

        media_body=MediaFileUpload(file_to_upload)
    )
    response = request.execute()

    print(response)


# TODO При инициализации напрямую ($python video_uploader.py) скрипт отрабатывает нормально
if __name__ == "__main__":
    main()


class CronYoutubeUploader(CronJobBase):
    RUN_EVERY_MINS = 1
    MIN_NUM_FAILURES = 3
    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'youtube_uploader.CronYoutubeUploader'

    # TODO Проблема: при запуске uploader'a через cron, скрипт схлопывается - не происходит запрос на ввод гуглотокена
    def do(self):
        print(f"CronYoutubeUploader started at {time.strftime('%D %H:%M:%S')}\n")
        main()  # TODO Проблема: при инициализации отсюда происходит НиХуЯ
        print(f"\nCronYoutubeUploader finished at {time.strftime('%D %H:%M:%S')}")
