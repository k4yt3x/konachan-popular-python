#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (C) 2022 K4YT3X and contributors.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as
published by the Free Software Foundation, only version 2
of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import contextlib
from datetime import datetime
from typing import List

import requests
from loguru import logger
from telegram import InputMediaPhoto
from telegram.ext import AIORateLimiter, ExtBot

from . import __version__

# format string for Loguru loggers
LOGURU_FORMAT = (
    "<green>{time:HH:mm:ss.SSSSSS!UTC}</green> | "
    "<level>{level: <8}</level> | "
    "<level>{message}</level>"
)

# the maximum file size Telegram can automatically download with a URL
TELEGRAM_MAX_DOWNLOAD_SIZE = 5 * 1024**2


def groups(l: list, n: int):
    for i in range(0, len(l), n):
        yield l[i : i + n]


class KonachanPopular:
    def __init__(self, token: str, chat_id: str) -> None:
        self.bot = ExtBot(token, rate_limiter=AIORateLimiter(max_retries=5))
        self.chat_id = chat_id

    @staticmethod
    def _get_konachan_popular() -> list:
        """
        retrieve the list of popular posts from Konachan.com using their Moebooru API

        :rtype list: the list of dicts that each describes a post
        """
        return requests.get("https://konachan.com/post/popular_recent.json").json()

    async def _send_posts(self, posts: List[InputMediaPhoto]):
        """
        send a list of InputMediaPhoto as an album into the chat

        :param posts List[InputMediaPhoto]: the list of images to send
        """
        await self.bot.send_media_group(self.chat_id, posts, read_timeout=60)

    async def send_popular(self):
        """
        send the popular posts in the past 24 hours into the chat

        """
        date = datetime.utcnow().strftime("%B %-d, %Y")
        logger.info(f"retrieving posts for {date}")

        # all of the InputMediaPhoto objects to send
        posts: List[InputMediaPhoto] = []

        # for each popular post
        for post in self._get_konachan_popular():

            # skip if error occurred
            with contextlib.suppress(Exception):

                # if the original file's size is smaller than the max tolerable size
                if post["file_size"] < TELEGRAM_MAX_DOWNLOAD_SIZE:
                    posts.append(InputMediaPhoto(post["jpeg_url"]))

                # if the sample file's size is smaller than the max tolerable size
                elif post["sample_file_size"] < TELEGRAM_MAX_DOWNLOAD_SIZE:
                    posts.append(InputMediaPhoto(post["sample_url"]))

                # otherwise skip this post as it is too big

        # send today's date
        await self.bot.send_message(self.chat_id, date)

        # send posts in groups of 10 (max number of images per media group)
        for group in groups(posts, 10):
            await self._send_posts(group)
