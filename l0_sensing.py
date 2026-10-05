from __future__ import annotations

import math
from dataclasses import dataclass

from cell_env import Env, PhysSig


@dataclass(frozen=True)
class Probe:
    turn: float
    signal: PhysSig


@dataclass(frozen=True)
class Afferent:
    intake: float
    harm: float
    touch: float
    seek_turn: float
    evade_turn: float


@dataclass(frozen=True)
class Sense:
    here: PhysSig
    left: Probe
    forward: Probe
    right: Probe
    contact: bool

    @property
    def nutrient_bias(self) -> float:
        return _clamp(self.right.signal.nutrient - self.left.signal.nutrient, -1.0, 1.0)

    @property
    def harmful_bias(self) -> float:
        return _clamp(self.right.signal.harmful - self.left.signal.harmful, -1.0, 1.0)

    def afferent(self) -> Afferent:
        touch = max(self.here.touch, self.left.signal.touch, self.forward.signal.touch, self.right.signal.touch)
        if self.contact:
            touch = 1.0
        return Afferent(
            intake=_clamp(self.here.nutrient * 0.65 + self.forward.signal.nutrient * 0.35, 0.0, 1.0),
            harm=_clamp(max(self.here.harmful, self.forward.signal.harmful), 0.0, 1.0),
            touch=_clamp(touch, 0.0, 1.0),
            seek_turn=self.nutrient_bias,
            evade_turn=_clamp(touch * 0.6 - self.harmful_bias, -1.0, 1.0),
        )


class SenseOrgan:
    def __init__(self, distance: float = 18.0, turn_angle: float = 0.62) -> None:
        self.distance = distance
        self.turn_angle = turn_angle

    def scan(self, env: Env, x: float, y: float, heading: float, radius: float) -> Sense:
        here = env.sample(x, y)
        probes = []
        for turn in (-self.turn_angle, 0.0, self.turn_angle):
            angle = heading + turn
            signal = env.sample(x + math.cos(angle) * self.distance, y + math.sin(angle) * self.distance)
            probes.append(Probe(turn=turn, signal=signal))
        return Sense(here, probes[0], probes[1], probes[2], env.touches(x, y, radius))


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))

