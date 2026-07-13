import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts, converting numeric fields to int/float."""
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

GENRE_WEIGHT = 25.0
MOOD_WEIGHT = 25.0
ENERGY_WEIGHT = 30.0
ACOUSTIC_WEIGHT = 20.0

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user_prefs: genre match (+25), mood match (+25), energy closeness (+30 max), acousticness fit (+20 max); returns (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    favorite_genre = user_prefs.get("genre")
    if favorite_genre and song.get("genre") == favorite_genre:
        score += GENRE_WEIGHT
        reasons.append(f"genre match ({favorite_genre}) (+{GENRE_WEIGHT:.1f})")

    favorite_mood = user_prefs.get("mood")
    if favorite_mood and song.get("mood") == favorite_mood:
        score += MOOD_WEIGHT
        reasons.append(f"mood match ({favorite_mood}) (+{MOOD_WEIGHT:.1f})")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        energy_diff = min(abs(song.get("energy", 0.0) - target_energy), 1.0)
        energy_points = ENERGY_WEIGHT * (1 - energy_diff)
        score += energy_points
        reasons.append(f"energy closeness (+{energy_points:.1f})")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        acousticness = song.get("acousticness", 0.0)
        acoustic_points = ACOUSTIC_WEIGHT * (acousticness if likes_acoustic else 1 - acousticness)
        score += acoustic_points
        reasons.append(f"acousticness fit (+{acoustic_points:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song against user_prefs and return the top k as (song, score, explanation), sorted highest first."""
    scored = [
        (song, score, "; ".join(reasons) if reasons else "no strong matches")
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda entry: entry[1], reverse=True)[:k]
