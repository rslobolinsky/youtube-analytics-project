import datetime
from datetime import timedelta

import isodate

from src.mixins import YoutubeMixin


class Playlist(YoutubeMixin):
    def __init__(self, id_playlist, ):
        self.id_playlist: str = id_playlist
        info = self.get_service().playlistItems().list(playlistId=self.id_playlist,
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
