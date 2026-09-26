from canonical_engine import CanonicalPST, CONFIG


def test_contract():
    assert CONFIG["version"] == "PST-CANONICAL-1.0"
    assert CONFIG["transition_weights"] == {"P": 0.05, "S": 0.04, "T": 0.03}
    assert CONFIG["initial_state"] == {"P": 0.88, "S": 0.78, "T": 0.40}
    assert CONFIG["bounds"]["T"] == [0.10, 0.80]


def test_first_transition():
    result = CanonicalPST().step(0.85, 0.75)
    assert result["P"] == 0.9055
    assert result["S"] == 0.8062
    assert result["T"] == 0.4494
