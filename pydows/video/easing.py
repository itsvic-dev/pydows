from typing import Callable
from ..constants import Duration
from ..helpers import get_duration


def ease_out_expo(x: float) -> float:
    return 1 if x == 1 else 1 - pow(2, -10 * x)


def do_ease(pos1: tuple[int, int], pos2: tuple[int, int], duration: Duration, ease_func: Callable[[float], float],
            fps=60):
    """
    Ease between 2 positions for n frames.
    :param pos1: source position
    :param pos2: target position
    :param duration: interpolate duration
    :param ease_func: easing function
    :param fps: FPS of the scene
    :return: list of position keyframes
    """
    positions = []
    duration = get_duration(duration, fps=fps)

    time_step = 1 / duration
    for i in range(duration):
        dist = ease_func(time_step * i)
        positions.append((
            round(pos1[0] + dist * (pos2[0] - pos1[0])),
            round(pos1[1] + dist * (pos2[1] - pos1[1])),
        ))

    return positions
