from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_CONFIG = Path(__file__).with_name("canonical_weights.json")
CONFIG = json.loads(_CONFIG.read_text(encoding="utf-8"))


@dataclass
class CanonicalPST:
    P: float = CONFIG["initial_state"]["P"]
    S: float = CONFIG["initial_state"]["S"]
    T: float = CONFIG["initial_state"]["T"]

    def step(self, pressure: float, novelty: float) -> dict[str, float | str]:
        if not 0 <= pressure <= 1 or not 0 <= novelty <= 1:
            raise ValueError("pressure_and_novelty_must_be_in_0_1")

        w = CONFIG["transition_weights"]
        self.P = self._clip(self.P + w["P"] * pressure * (1 - self.T), "P")
        self.S = self._clip(
            self.S + w["S"] * novelty * (1 - abs(self.P - self.S)), "S"
        )
        self.T = self._clip(
            self.T + w["T"] * (self.S / (self.P + 1e-9)) * (1 + pressure), "T"
        )
        return {
            "P": round(self.P, 4),
            "S": round(self.S, 4),
            "T": round(self.T, 4),
            "energy": round(self.energy(), 4),
            "phase": self.phase(),
        }

    @staticmethod
    def _clip(value: float, axis: str) -> float:
        low, high = CONFIG["bounds"][axis]
        return min(max(value, low), high)

    def energy(self) -> float:
        return (self.P * self.S) / (1.1 - self.T + 1e-9) * (
            1 - self.T / (self.P + self.S + 1e-9)
        )

    def phase(self) -> str:
        t = CONFIG["phase_thresholds"]
        if abs(self.P - self.S) < t["rupture_distance"]:
            return "RUPTURE_IMMINENT"
        if self.T < t["unstable_T"]:
            return "UNSTABLE_CREATIVITY"
        if self.P > t["synthesis_P"] and self.S > t["synthesis_S"]:
            return "SYNTHESIS_PEAK"
        return "STEADY_EXPLORATION"
