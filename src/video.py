import os

from googleapiclient.discovery import build


class Video:
    """Класс для видео с YouTube"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """
        :param: video_id: id видео
        :param: video_title: название видео
        :param: view_count: количество просмотров видео
        :param: like_count: количество лайков на видео
        :param: comment_count: количество комментариев под видео

        """
        self.video_id: str = video_id
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=self.video_id
                                                    ).execute()
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = video_response['items'][0]['statistics']['commentCount']

    def __str__(self):
        """Магический метод (__str__) который выводит название видео"""
        return self.video_title


class PLVideo(Video):
    """Класс для плейлиста с YouTube"""

    def __init__(self, video_id: str, playlist_id: str) -> None:
        """
        :param playlist_id: id плейлиста
        """
        super().__init__(video_id)
        self.playlist_id: str = playlist_id
