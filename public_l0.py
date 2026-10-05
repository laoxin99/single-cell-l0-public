from __future__ import annotations

from dataclasses import dataclass
from random import Random

from cell_env import Env
from l0_sensing import Afferent, SenseOrgan


@dataclass
class PublicCell:
    """A small, headless public fixture derived from the L0 physiology concepts."""

    x: float = 68.0
    y: float = 90.0
    heading: float = 0.0
    reserve: float = 0.62
    energy: float = 0.62
    support: float = 0.92
    mass: float = 1.0
    age: int = 0
    divisions: int = 0

    radius: float = 6.0

    def step(self, env: Env, sensor: SenseOrgan) -> str:
        sense = sensor.scan(env, self.x, self.y, self.heading, self.radius)
        aff = sense.afferent()
        behavior = self._choose_behavior(aff)
        if behavior == "avoid":
            self.heading += 0.45 if aff.evade_turn >= 0 else -0.45
            speed = 2.0
        elif behavior == "approach":
            self.heading += aff.seek_turn * 0.28
            speed = 1.2
        else:
            speed = 0.15

        next_x = max(self.radius, min(env.width - self.radius, self.x + speed))
        if not env.touches(next_x, self.y, self.radius):
            self.x = next_x

        intake = 0.022 * aff.intake if behavior != "avoid" else 0.006 * aff.intake
        maintenance = 0.004
        self.reserve = min(1.0, self.reserve + intake - 0.002)
        self.energy = min(1.0, self.energy + self.reserve * 0.004 - maintenance - aff.harm * 0.006)
        self.support = max(0.0, min(1.0, self.support + 0.001 * aff.intake - aff.harm * 0.003 - aff.touch * 0.001))
        self.mass = min(2.0, self.mass + 0.05 * aff.intake)
        self.age += 1

        if self.age >= 21 and self.mass >= 1.45 and self.energy >= 0.54 and self.support >= 0.84:
            self.mass = 1.0
            self.reserve *= 0.62
            self.energy *= 0.66
            self.divisions += 1
            return f"{behavior}+division"
        return behavior

    @staticmethod
    def _choose_behavior(aff: Afferent) -> str:
        if aff.harm >= 0.30 or aff.touch >= 0.72:
            return "avoid"
        if aff.intake >= 0.16:
            return "approach"
        return "drift"


def run_fixture(seed: int) -> dict[str, int | str]:
    # The fixed fixture intentionally uses only local deterministic inputs.
    rng = Random(seed)
    env = Env()
    cell = PublicCell(x=68.0 + rng.uniform(-2.0, 2.0), y=90.0)
    sensor = SenseOrgan()
    first_division = None
    behavior_counts: dict[str, int] = {}
    for step in range(1, 22):
        behavior = cell.step(env, sensor)
        behavior_counts[behavior] = behavior_counts.get(behavior, 0) + 1
        if cell.divisions and first_division is None:
            first_division = step
        env.step()
    return {
        "seed": seed,
        "first_division": first_division or 0,
        "division_count": cell.divisions,
        "steps": 21,
        "behaviors": ",".join(sorted(behavior_counts)),
    }


def main() -> None:
    results = [run_fixture(seed) for seed in range(101, 121)]
    successful = sum(result["division_count"] == 1 for result in results)
    first_steps = sorted(int(result["first_division"]) for result in results if result["first_division"])
    median = first_steps[len(first_steps) // 2] if first_steps else 0
    print("fixture=l0-public-minimal")
    print("dependencies=python-standard-library+2-local-modules")
    print(f"runs={len(results)}")
    print(f"division={successful}/{len(results)}")
    print(f"median_first_division={median}")
    print("boundary=fixture-only; not a full project runtime")


if __name__ == "__main__":
    main()

