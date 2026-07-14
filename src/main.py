"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    # --- Distinct, "realistic" taste profiles ---
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.3,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    # --- Adversarial / edge-case profiles ---
    # Conflicting signals: "sad" isn't a mood in the catalog (closest is
    # "melancholic"), and pairing it with near-max energy is contradictory —
    # does the recommender still confidently return a top 5?
    "Conflicting Signals (sad + high energy)": {
        "genre": "rock",
        "mood": "sad",
        "energy": 0.95,
        "likes_acoustic": False,
    },
    # Unknown genre: "vaporwave" does not exist in data/songs.csv, so genre
    # can never match. Tests that scoring degrades gracefully instead of
    # erroring or returning nothing.
    "Unknown Genre (vaporwave)": {
        "genre": "vaporwave",
        "mood": "chill",
        "energy": 0.4,
        "likes_acoustic": True,
    },
    # Empty profile: no preferences at all. Every song should score 0, so
    # this checks that ties are broken predictably (e.g. by catalog order)
    # rather than crashing.
    "Empty Profile": {},
    # Out-of-range energy: 5.0 is far outside the expected 0-1 scale. Tests
    # whether the energy-closeness calculation clamps correctly instead of
    # producing a negative or nonsensical score.
    "Out-of-Range Energy": {
        "genre": "pop",
        "mood": "happy",
        "energy": 5.0,
        "likes_acoustic": False,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in PROFILES.items():
        print(f"\n=== Profile: {profile_name} ===")
        print(f"Preferences: {user_prefs}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\nTop recommendations:\n")
        for rec in recommendations:
            # You decide the structure of each returned item.
            # A common pattern is: (song, score, explanation)
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
