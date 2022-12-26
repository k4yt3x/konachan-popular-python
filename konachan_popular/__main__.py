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

import argparse
import asyncio
import os
import sys

from loguru import logger

from .konachan_popular import LOGURU_FORMAT, KonachanPopular


def parse_arguments() -> argparse.Namespace:
    """
    parse command line arguments

    :rtype argparse.Namespace: command parsing results
    """
    parser = argparse.ArgumentParser(
        prog="konachan-popular",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-t",
        "--token",
        help="Telegram bot API token",
        required=os.environ.get("TELOXIDE_TOKEN") is None,
        default=os.environ.get("TELOXIDE_TOKEN"),
    )
    parser.add_argument(
        "-c",
        "--chat-id",
        help="ID of the chat to send messages to",
        required=os.environ.get("TELOXIDE_CHAT_ID") is None,
        default=os.environ.get("TELOXIDE_CHAT_ID"),
    )
    return parser.parse_args()


def main() -> int:
    """
    command line entrypoint for direct CLI invocation

    :rtype int: 0 if completed successfully, else other int
    """

    try:
        # parse command line arguments
        args = parse_arguments()

        # remove default handler
        logger.remove()

        # add new sink with custom handler
        logger.add(sys.stderr, colorize=True, format=LOGURU_FORMAT)

        konachan_popular = KonachanPopular(args.token, args.chat_id)
        asyncio.run(konachan_popular.send_popular())

    # don't print the traceback for manual terminations
    except KeyboardInterrupt:
        return 2

    except Exception as error:
        logger.exception(error)
        return 1

    # if no exceptions were produced
    else:
        logger.success("Program finished successfully")
        return 0


if __name__ == "__main__":
    sys.exit(main())
