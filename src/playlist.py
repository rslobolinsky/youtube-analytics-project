import datetime
from datetime import timedelta

from poetry.console.commands import self

#import isodate

from src.channel import Channel


class PlayList(Channel):
    def __init__(self, id_playlist,):
        self.id_playlist: str = id_playlist
        #self._total_duration: datetime = None
        self.make_attribute_info()

    def make_attribute_info(self) -> None:
       """Make attribute for __init__"""
       youtube = self.get_service()
       info =youtube.playlistItems().list(playlistId = self.id_playlist,
                                            part="snippet,contentDetails").execute()
       playlists = self.get_service().playlists().list(id=self.id_playlist,
                                                        part='snippet',
                                                        ).execute()
       self.title: str = playlists['items'][0]['snippet']['title']
       self.url: str = f"https://www.youtube.com/playlist?list={self.id_playlist}"
       video_ids: list[str] = [video['contentDetails']['videoId'] for video in info['items']]
       self.video_response: dict = self.get_service().videos().list(part='contentDetails,statistics',
                                                                     id=','.join(video_ids)
                                                                     ).execute()


    @property
    def total_duration(self) -> datetime:
        _total_duration: timedelta = datetime.timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            _total_duration += duration
        return _total_duration


    def show_best_video(self) -> str:
        """Get info about videos and search the best video with more likes than
        other videos.
        :return: url the best video"""
        max_likes: int = 0
        best_video_id: str = ''
        for info in self.video_response['items']:
            if int(info['statistics']['likeCount']) > max_likes:
                max_likes: int = int(info['statistics']['likeCount'])
                best_video_id: str = info['id']

        return f"https://youtu.be/{best_video_id}"

    #def get_info(self) -> list[str]:
    #def get_info(self) -> dict:
    #     """Get API request from youtube"""
    #     youtube = self.get_service()
    #     return youtube.playlistItems().list(playlistId=self.id_playlist,
    #                                         part="snippet,contentDetails").execute()
    #
    # def make_attribute_info(self) -> None:
    #     """Make attribute for __init__"""
    #     info = self.get_info()
    #     self.title: str = info['items'][0]['snippet']['title']
    #     self.url: str = f"https://www.youtube.com/playlist?list={self.id_playlist}"
    #     self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in info['items']]
    #
    # def get_duration_videos(self) -> None:
    #     """Get video's duration and make self._total_duration"""
    #     youtube = self.get_service()
    #     self.video_response: list[str] = youtube.videos().list(part='contentDetails,statistics',
    #                                                            id=','.join(self.video_ids)
    #                                                            ).execute()
    #
    #     self._total_duration = datetime.timedelta()
    #
    #     for video in self.video_response['items']:
    #         # YouTube video duration is in ISO 8601 format
    #         iso_8601_duration = video['contentDetails']['duration']
    #         duration = isodate.parse_duration(iso_8601_duration)
    #         self._total_duration += duration
    #
    # @property
    # def total_duration(self) -> datetime:
    #     return self._total_duration
    #
    # def show_best_video(self) -> str:
    #     """Get info about videos and search the best video with more likes than
    #     other videos.
    #     :return: url the best video"""
    #     youtube = self.get_service()
    #
    #     video_response: list = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
    #                                                  id=','.join(self.video_ids)
    #                                                  ).execute()
    #     max_likes: int = 0
    #
    #     best_video_id: str = ''
    #
    #     for info in video_response['items']:
    #         if int(info['statistics']['likeCount']) > max_likes:
    #             max_likes: int = int(info['statistics']['likeCount'])
    #             best_video_id: str = info['id']
    #
    #     return f"https://www.youtube.com/watch?v={best_video_id}"