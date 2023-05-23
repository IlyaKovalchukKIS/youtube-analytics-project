import json
import os

import google
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        self.__channel_id = channel_id
        self.title = channel['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/channel/{channel_id}'
        self.count_subscribers = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.count_subscribers) + int(other.count_subscribers)

    def __sub__(self, other):
        return int(self.count_subscribers) - int(other.count_subscribers)

    def __gt__(self, other):
        return int(self.count_subscribers) > int(other.count_subscribers)

    def __ge__(self, other):
        return int(self.count_subscribers) >= int(other.count_subscribers)

    @classmethod
    def get_service(cls):
        """Возвращающий объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=cls.api_key)

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        with open(filename, "w") as f:
            json.dump(self.__dict__, f, indent=2)

