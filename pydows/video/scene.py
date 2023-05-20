import os
import random
import shutil
from enum import Enum
import string
import tqdm
from pydows.views import View, LayeredView
from moviepy import ImageSequenceClip, AudioFileClip, CompositeAudioClip


class Scene(View):
    def __init__(self, main_view: View, offset=0):
        super().__init__()
        self.main_view = main_view
        self.actions = []
        self.audio_clips = []
        self.duration = 0
        self.fps = 60
        self._offset = offset
        self._current_frame = -1
        self._current_start = -1

    def get_size(self) -> tuple[int, int] | tuple[float, float]:
        return self.main_view.get_size()

    class Action:
        class Type(Enum):
            ADD_CHILD = 0,
            WAIT_FRAMES = 2,

        def __init__(self, _type: Type, start_frame: int, end_frame=-1, child: View | None = None,
                     position: tuple[int, int] | None = None, keyframes: list[tuple[int, int]] | None = None):
            self.type = _type
            self.start_frame = start_frame
            self.end_frame = end_frame
            self.child = child
            self.keyframes = keyframes
            self.position = position

        def applies_to_frame(self, frame: int):
            if self.end_frame == -1:
                return frame >= self.start_frame
            else:
                return self.start_frame <= frame < self.end_frame

    def add_child(self, child: View, after_n_frames=0, keyframes: list[tuple[int, int]] | None = None,
                  position: tuple[int, int] | None = None, duration=None, is_async=False):
        if keyframes is None:
            keyframes = []
        if duration is None and len(keyframes) != 0:
            duration = len(keyframes)
        elif duration is None:
            duration = 0

        start_frame = self.duration + after_n_frames
        if duration == 0:
            end_frame = -1
        else:
            end_frame = start_frame + duration

        action = self.Action(self.Action.Type.ADD_CHILD, start_frame, end_frame, child=child, position=position,
                             keyframes=keyframes)
        self.actions.append(action)
        if not is_async and (duration or keyframes):
            self.actions.append(self.Action(self.Action.Type.WAIT_FRAMES, start_frame, end_frame))
            self.duration += (duration or len(keyframes)) + after_n_frames

    def wait_n_frames(self, n: int):
        start_frame = self.duration
        end_frame = start_frame + n
        self.actions.append(self.Action(self.Action.Type.WAIT_FRAMES, start_frame, end_frame))
        self.duration += n

    def play_audio(self, file: str, after_n_frames=0):
        self.audio_clips.append(AudioFileClip(file).with_start((self.duration + after_n_frames) / self.fps))

    def _paint(self, n: int):
        self._current_frame = n
        view = LayeredView()
        view.parent = self
        view.add_child(self.main_view, is_main=True)

        for action in self.actions:
            if not action.applies_to_frame(n):
                continue
            if action.child:
                # get child position
                position = action.position
                if action.keyframes and n - action.start_frame < len(action.keyframes):
                    position = action.keyframes[n - action.start_frame]
                if not position and action.keyframes:
                    # use last keyframe as fallback
                    position = action.keyframes[-1]
                view.add_child(action.child, xy=position)

        return view.paint()

    def paint(self):
        if not self.parent:
            raise NotImplementedError("Scene::paint() requires a parent. Did you mean to use render()?")
        current_frame = self.parent.get_custom_property("current_frame")
        frame = (current_frame - self._offset) % self.duration
        return self._paint(frame)

    def render(self, file: str, preset="veryslow"):
        tmpdir = f"/tmp/" + "".join(random.choices(string.ascii_letters, k=8))
        os.mkdir(tmpdir)
        for i in tqdm.tqdm(range(self.duration), desc="scene frame rendering", total=self.duration):
            self._paint(i).save(f"{tmpdir}/{i:05d}.bmp")

        clip = ImageSequenceClip(tmpdir, fps=self.fps)
        if self.audio_clips:
            clip.audio = CompositeAudioClip(self.audio_clips).with_duration(clip.duration)
        clip.write_videofile(file, preset=preset)

        shutil.rmtree(tmpdir)

    def get_custom_property(self, prop: str):
        if prop == "current_frame":
            return self._current_frame
