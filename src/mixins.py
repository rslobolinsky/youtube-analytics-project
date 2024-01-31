import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class YoutubeMixin:
    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API.
        """
        return build('youtube', 'v3', developerKey=os.getenv("KEY_API_YOUTUBE"))