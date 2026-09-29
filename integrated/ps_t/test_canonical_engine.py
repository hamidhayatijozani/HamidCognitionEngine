import pytest

from canonical_engine import CanonicalPST, CONFIG


def test_contract():
    assert CONFIG["version"] == "PST-CANONICAL-1.0"
    assert CONFIG["transition_weights"] == {"P": 0.05, "S": 0.04, "T": 0.03}
    assert CONFIG["initial_state"] == {"P": 0.88, "S": 0.78, "T": 0.40}
    assert CONFIG["bounds"] == {
        "P": [0.10, 0.95],
        "S": [0.10, 0.95],
        "T": [0.10, 0.80],
    }


def test_first_transition_regression_vector():
    result = CanonicalPST().step(0.85, 0.75)
    assert result == {
        "P": 0.9055,
        "S": 0.8062,
        "T": 0.4494,
        "energy": 0.8275,
        "phase": "RUPTURE_IMMINENT",
    }


def test_multistep_trajectory_is_deterministic():
    inputs = [(0.85, 0.75), (0.40, 0.60), (0.90, 0.20)]
    engine = CanonicalPST()
    trajectory = [engine.step(*pair) for pair in inputs]
    assert trajectory == [
        {"P": 0.9055, "S": 0.8062, "T": 0.4494, "energy": 0.8275, "phase": "RUPTURE_IMMINENT"},
        {"P": 0.9165, "S": 0.8276, "T": 0.4873, "energy": 0.8921, "phase": "RUPTURE_IMMINENT"},
        {"P": 0.9396, "S": 0.8347, "T": 0.5380, "energy": 0.9723, "phase": "RUPTURE_IMMINENT"},
    ]


@pytest.mark.parametrize("pressure,novelty", [(-0.01, 0.5), (0.5, -0.01), (1.01, 0.5), (0.5, 1.01)])
def test_inputs_outside_contract_are_rejected(pressure, novelty):
    with pytest.raises(ValueError, match="pressure_and_novelty_must_be_in_0_1"):
        CanonicalPST().step(pressure, novelty)


def test_state_stays_inside_declared_bounds_after_extreme_inputs():
    engine = CanonicalPST()
    for _ in range(100):
        result = engine.step(1.0, 1.0)
        assert CONFIG["bounds"]["P"][0] <= result["P"] <= CONFIG["bounds"]["P"][1]
        assert CONFIG["bounds"]["S"][0] <= result["S"] <= CONFIG["bounds"]["S"][1]
        assert CONFIG["bounds"]["T"][0] <= result["T"] <= CONFIG["bounds"]["T"][1]


def test_new_instances_are_independent():
    a = CanonicalPST()
    b = CanonicalPST()
    a.step(1.0, 1.0)
    assert (a.P, a.S, a.T) != (b.P, b.S, b.T)
    assert (b.P, b.S, b.T) == (0.88, 0.78, 0.40)
