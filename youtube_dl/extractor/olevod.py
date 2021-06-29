# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class OlevodIE(InfoExtractor):
    _BASE_URL = "https://www.olevod.com"
    _VALID_URL = r'https?://www.olevod.com/index.php/vod/play/id/(?P<id>[0-9]+/sid/[0-9]+/nid/[0-9]+).html'
    _TESTS = [
        {
            'url': 'https://www.olevod.com/index.php/vod/play/id/27132/sid/1/nid/1.html',
            'md5': '2bb59c7b80de43ee58b6513eb37f7d68',
            'info_dict': {
                'id': '27132-1-1',
                'ext': 'mp4',
                'title': '速度与激情9',
                'thumbnail': r're:^https://www.olevod.com/upload/vod/.*?/.*?\.jpg$'
            }
        },
        {
            'url': 'https://www.olevod.com/index.php/vod/play/id/24119/sid/1/nid/1.html',
            'md5': '22ac1240171814a7df1f180e747ca180',
            'info_dict': {
                'id': '24119-1-1',
                'ext': 'mp4',
                'title': '旺达幻视_第01集',
                'thumbnail': r're:^https://www.olevod.com/upload/vod/.*?/.*?\.jpg$'
            }
        }]

    def _real_extract(self, url):
        vid_string = self._match_id(url)
        vid_string = vid_string.replace("/sid/", "-")
        video_id = vid_string.replace("/nid/", "-")
        webpage = self._download_webpage(url, video_id)

        title = self._html_search_regex(r'(?<=<title>)(?P<title>.*?)(?=\s-\s欧乐影院)',
                                        webpage, 'title')
        title = title.rstrip("_在线播放")
        thumbnail = self._html_search_regex(
            r"(?<=<div class=\"play_vlist_thumb vnow lazyload\" data-original=\")(?P<thumbnail>.*?\.jpg)(?=\"><\/div>)",
            webpage,
            'thumbnail')
        thumbnail = self._BASE_URL + thumbnail

        player_json = self._html_search_regex(
            r"(?<=var player_x10d26=)(?P<player_json>.*?)(?=</script>)",
            webpage,
            'player_json')
        player = self._parse_json(player_json, video_id)
        m3u8_url = player.get("url")

        formats = self._extract_m3u8_formats(m3u8_url,
                                             video_id,
                                             'mp4',
                                             m3u8_id='hls')

        return {
            'id': video_id,
            'title': title,
            'thumbnail': thumbnail,
            "formats": formats
        }
