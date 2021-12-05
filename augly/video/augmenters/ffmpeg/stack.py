#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.

from typing import List, Optional

from augly.utils import pathmgr
from augly.video.augmenters.ffmpeg.base_augmenter import BaseVidgearFFMPEGAugmenter
from augly.video.helpers import get_video_info


class VideoAugmenterByStack(BaseVidgearFFMPEGAugmenter):
    def __init__(
        self, second_video_path: str, use_second_audio: bool, orientation: str
    ):
        assert (
            type(use_second_audio) == bool
        ), "Expected a boolean value for use_second_audio"
        assert orientation in [
            "hstack",
            "vstack",
        ], "Expected orientation to be either 'hstack' or 'vstack'"

        self.second_video_path = pathmgr.get_local_path(second_video_path)
        self.use_second_audio = use_second_audio
        self.orientation = orientation

    def get_command(
        self, video_path: str, output_path: Optional[str] = None,
    ) -> List[str]:
        """
        Stacks two videos together

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @returns: a list of strings of the FFMPEG command if it were to be written
            in a command line
        """
        video_info = get_video_info(video_path)

        command = [
            "-y",
            "-i",
            video_path,
            "-i",
            self.second_video_path,
            "-filter_complex",
            f"[1:v]scale={video_info['width']}:{video_info['height']}[1v];"
            + f"[0:v][1v]{self.orientation}=inputs=2[v]",
            "-map",
            "[v]",
            "-map",
            f"{int(not self.use_second_audio)}:a",
            "-vsync",
            "2",
            "-preset",
            "ultrafast",
            output_path,
        ]

        return command
