from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Zone:
    kind: str
    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1

    @property
    def center(self) -> tuple[float, float]:
        return ((self.x1 + self.x2) / 2.0, (self.y1 + self.y2) / 2.0)


@dataclass(frozen=True)
class PhysSig:
    nutrient: float
    harmful: float
    touch: float
    obstacle: bool
    boundary: bool


class Env:
    """Small deterministic physical field used by the public fixture."""

    def __init__(self, width: int = 240, height: int = 180) -> None:
        self.width = width
        self.height = height
        self.nutrient_zones = [Zone("nutrient", 24, 54, 112, 126)]
        self.harmful_zones = [Zone("harmful", 160, 24, 226, 84)]
        self.obstacle_zones = [Zone("obstacle", 126, 108, 156, 168)]

    def sample(self, x: float, y: float) -> PhysSig:
        return PhysSig(
            nutrient=self._field_strength(self.nutrient_zones, x, y),
            harmful=self._field_strength(self.harmful_zones, x, y),
            touch=self._touch_strength(x, y),
            obstacle=self._point_hits(self.obstacle_zones, x, y),
            boundary=x <= 0 or y <= 0 or x >= self.width or y >= self.height,
        )

    def touches(self, x: float, y: float, radius: float) -> bool:
        if x - radius <= 0 or y - radius <= 0:
            return True
        if x + radius >= self.width or y + radius >= self.height:
            return True
        return any(self._circle_hits_rect(x, y, radius, zone) for zone in self.obstacle_zones)

    def step(self) -> None:
        # The public fixture has no hidden resource ledger; the field is fixed.
        return None

    @staticmethod
    def _field_strength(zones: list[Zone], x: float, y: float) -> float:
        best = 0.0
        for zone in zones:
            cx, cy = zone.center
            reach = max(zone.width, zone.height) * 1.2
            best = max(best, 1.0 - math.hypot(x - cx, y - cy) / reach)
        return max(0.0, min(1.0, best))

    def _touch_strength(self, x: float, y: float) -> float:
        boundary_distance = min(x, y, self.width - x, self.height - y)
        boundary = max(0.0, 1.0 - boundary_distance / 24.0)
        obstacle = 0.0
        for zone in self.obstacle_zones:
            nx = min(max(x, zone.x1), zone.x2)
            ny = min(max(y, zone.y1), zone.y2)
            obstacle = max(obstacle, 1.0 - math.hypot(x - nx, y - ny) / 30.0)
        return max(0.0, min(1.0, max(boundary, obstacle)))

    @staticmethod
    def _point_hits(zones: list[Zone], x: float, y: float) -> bool:
        return any(zone.x1 <= x <= zone.x2 and zone.y1 <= y <= zone.y2 for zone in zones)

    @staticmethod
    def _circle_hits_rect(x: float, y: float, radius: float, zone: Zone) -> bool:
        nx = min(max(x, zone.x1), zone.x2)
        ny = min(max(y, zone.y1), zone.y2)
        return math.hypot(x - nx, y - ny) <= radius

