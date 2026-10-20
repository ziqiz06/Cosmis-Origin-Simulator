"""Tests for the physics and habitability model in simulation.py."""
import itertools

import pytest

from cosmic_origins.simulation import HABITABLE_ZONES, build_world, calc_temp, in_hz

STARS = ["M", "K", "G", "F"]
DISTANCES = [0.1, 0.5, 1.0, 2.0, 5.2]


def _all_worlds():
    """A grid of worlds covering every journey and every categorical choice."""
    for journey, star, dist, atm, water, mag, geo, impact, moon, tidal, n in itertools.product(
        ["rocky", "earth_like", "icy_moon", "gas_giant", "star_system"],
        STARS, [0.3, 1.0, 5.2],
        ["none", "thin", "thick", "greenhouse"],
        ["none", "ice", "liquid", "abundant"],
        ["absent", "weak", "strong"],
        ["dead", "moderate", "active"],
        ["calm", "moderate", "heavy"],
        ["none", "small", "large"],
        ["none", "moderate", "strong"],
        [2, 8],
    ):
        yield build_world(journey, dict(
            star_type=star, distance_au=dist, atmosphere=atm, water=water,
            magnetic_field=mag, geology=geo, impact_history=impact, moon=moon,
            tidal_heating=tidal, num_planets=n,
            mass_earth=1000 if journey == "gas_giant" else 1.0,
        ))


# ── Physics ───────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("star", STARS)
def test_habitable_zone_boundaries_are_inclusive(star):
    inner, outer = HABITABLE_ZONES[star]
    assert in_hz(star, inner)
    assert in_hz(star, outer)
    assert not in_hz(star, inner * 0.9)
    assert not in_hz(star, outer * 1.1)


@pytest.mark.parametrize("star", STARS)
def test_planets_closer_to_their_star_are_hotter(star):
    temps = [calc_temp(star, d, "thin", "none") for d in DISTANCES]
    assert temps == sorted(temps, reverse=True)


def test_brighter_stars_heat_planets_more():
    temps = [calc_temp(star, 1.0, "thin", "none") for star in STARS]  # dimmest → brightest
    assert temps == sorted(temps)


# ── Habitability scoring ──────────────────────────────────────────────────────

def test_earth_like_defaults_confirm_life():
    earth = build_world("earth_like", {})
    assert earth.hab_label == "Life Confirmed"


def test_earth_label_requires_every_condition():
    assert build_world("earth_like", {"magnetic_field": "weak"}).hab_label != "Life Confirmed"
    assert build_world("earth_like", {"distance_au": 1.5}).hab_label != "Life Confirmed"


def test_scores_stay_in_range_for_every_choice_combination():
    for w in _all_worlds():
        assert 0 <= w.habitability_score <= 100, w


def test_score_breakdown_adds_up_to_score():
    """The result page's factor breakdown must explain the score it shows."""
    for w in _all_worlds():
        earned = sum(points for _, points, _ in w.score_explanation)
        if w.journey in ("rocky", "earth_like"):
            earned = max(0, min(100, earned))  # breakdown shows raw points; score is clamped
        if w.journey == "gas_giant" and w.moon == "none":
            continue  # no moons short-circuits to 0
        assert earned == w.habitability_score, (w.journey, w.mass_earth, earned, w.habitability_score)


def test_gas_giant_without_moons_cannot_host_moon_life():
    assert build_world("gas_giant", {"moon": "none"}).habitability_score == 0


def test_super_jupiter_is_penalised():
    jupiter = build_world("gas_giant", {"moon": "large", "mass_earth": 318})
    super_jupiter = build_world("gas_giant", {"moon": "large", "mass_earth": 1000})
    assert super_jupiter.habitability_score < jupiter.habitability_score


def test_moderate_tidal_heating_is_the_icy_moon_sweet_spot():
    scores = {t: build_world("icy_moon", {"tidal_heating": t}).habitability_score
              for t in ("none", "moderate", "strong")}
    assert scores["moderate"] > scores["strong"] > scores["none"]


# ── build_world ───────────────────────────────────────────────────────────────

def test_build_world_ignores_unknown_choice_keys():
    w = build_world("rocky", {"not_a_field": 123, "water": "liquid"})
    assert w.water == "liquid"
    assert not hasattr(w, "not_a_field")
