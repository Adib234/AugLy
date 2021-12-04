#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.

import math
from typing import List, Optional

from augly.video.augmenters.ffmpeg.base_augmenter import BaseVidgearFFMPEGAugmenter


class VideoAugmenterByRotation(BaseVidgearFFMPEGAugmenter):
    def __init__(self, degrees: float):
        assert isinstance(degrees, (float, int)), "Expected 'degrees' to be a number"
        self.degrees = degrees

    def get_command(
        self, video_path: str, output_path: Optional[str] = None, **kwargs
    ) -> List[str]:
        """
        Rotates the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @returns: a list of strings of the FFMPEG command if it were to be written
            in a command line
        """
        command = [
            "-y",
            "-i",
            video_path,
            "-vf",
            f"rotate={self.degrees * (math.pi / 180)}",
            "-c:a",
            "copy",
            "-preset",
            "ultrafast",
            output_path,
        ]
        return command
