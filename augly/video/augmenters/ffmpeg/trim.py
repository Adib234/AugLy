#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.

from typing import List, Optional

from augly.video.augmenters.ffmpeg.base_augmenter import BaseVidgearFFMPEGAugmenter
from augly.video.helpers import get_video_info


class VideoAugmenterByTrim(BaseVidgearFFMPEGAugmenter):
    def __init__(
        self,
        start: Optional[float] = None,
        end: Optional[float] = None,
        offset_factor: float = 0.0,
        duration_factor: float = 1.0,
    ):
        assert start is None or start >= 0, "Start cannot be a negative number"
        assert (
            end is None or (start is not None and end > start) or end > 0
        ), "End must be a value greater than start"
        assert (
            0.0 <= offset_factor <= 1.0
        ), "Offset factor must be a value in the range [0.0, 1.0]"
        assert (
            0.0 <= duration_factor <= 1.0
        ), "Duration factor must be a value in the range [0.0, 1.0]"

        if start is not None or end is not None:
            self.start = start
            self.end = end
            self.offset_factor = None
            self.duration_factor = None
        else:
            self.start = None
            self.end = None
            self.offset_factor = offset_factor
            self.duration_factor = duration_factor

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Trims the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.

        @returns: a list of strings of the FFMPEG command if it were to be written
            in a command line
        """
        video_info = get_video_info(video_path)
        duration = float(video_info["duration"])

        if self.start is None and self.end is None:
            self.start = self.offset_factor * duration
            duration = min(self.duration_factor * duration, duration - self.start)
            self.end = self.start + duration
        elif self.start is None:
            self.start = 0
        elif self.end is None:
            self.end = duration

        command = [
            "-y",
            "-i",
            video_path,
            "-vf",
            f"trim={self.start}:{self.end}," + "setpts=PTS-STARTPTS",
            "-af",
            f"atrim={self.start}:{self.end}," + "asetpts=PTS-STARTPTS",
            "-preset",
            "ultrafast",
            output_path,
        ]

        return command
