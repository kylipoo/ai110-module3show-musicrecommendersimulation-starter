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
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    print(f"Loading songs from {csv_path}...")
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(song: Dict, user_prefs: Dict) -> Tuple[float, str]:
    """
    Scores a single song against user preferences.
    Returns (score, explanation) where score is in [0.0, 1.0].

    Weights:
      0.40 genre match (binary)
      0.25 mood match  (binary)
      0.20 energy proximity
      0.10 tempo proximity
      0.05 acousticness fit
    """
    genre_score = 1.0 if song["genre"] == user_prefs["favorite_genre"] else 0.0
    mood_score  = 1.0 if song["mood"]  == user_prefs["favorite_mood"]  else 0.0

# These scores are converted in such a way that can be scaled [0, 1]

# Energy proximity is calculated as a linear decay from 1.0 at perfect match to 0.0 at 1.0 difference
    energy_score = max(0.0, 1.0 - abs(song["energy"] - user_prefs["target_energy"]))

# Tempo proximity is calculated as a linear decay from 1.0 at perfect match to 0.0 at 200 BPM difference
    tempo_score = max(0.0, 1.0 - abs(song["tempo_bpm"] - user_prefs["target_tempo"]) / 200.0)

    if user_prefs["likes_acoustic"]:
        acoustic_score = song["acousticness"]
    else:
        acoustic_score = 1.0 - song["acousticness"]

    # Original weights: genre=0.40, mood=0.25, energy=0.20, tempo=0.10, acousticness=0.05
    score = (
        0.40 * genre_score +
        0.25 * mood_score  +
        0.20 * energy_score +
        0.10 * tempo_score +
        0.05 * acoustic_score
    )

    # Energy-sensitive weights: genre halved (0.20), energy doubled (0.40)
    # score = (
    #     0.20 * genre_score +
    #     0.25 * mood_score  +
    #     0.40 * energy_score +
    #     0.10 * tempo_score +
    #     0.05 * acoustic_score
    # )

    reasons = []

    if genre_score == 1.0:
        reasons.append(f"genre matches ({song['genre']})")
    else:
        reasons.append(f"genre doesn't match (it's {song['genre']}, you want {user_prefs['favorite_genre']})")

    if mood_score == 1.0:
        reasons.append(f"mood matches ({song['mood']})")
    else:
        reasons.append(f"mood doesn't match (it's {song['mood']}, you want {user_prefs['favorite_mood']})")

    if energy_score >= 0.90:
        reasons.append(f"energy closely matches your target ({song['energy']} vs {user_prefs['target_energy']})")
    elif energy_score >= 0.70:
        reasons.append(f"energy is close but not exact ({song['energy']} vs target {user_prefs['target_energy']})")
    else:
        reasons.append(f"energy is far from your target ({song['energy']} vs {user_prefs['target_energy']})")

    if tempo_score >= 0.90:
        reasons.append(f"tempo closely matches ({song['tempo_bpm']} BPM vs target {user_prefs['target_tempo']})")
    elif tempo_score < 0.70:
        reasons.append(f"tempo is off ({song['tempo_bpm']} BPM vs target {user_prefs['target_tempo']})")

    if not user_prefs["likes_acoustic"] and song["acousticness"] > 0.5:
        reasons.append(f"more acoustic than you prefer (acousticness {song['acousticness']})")
    elif user_prefs["likes_acoustic"] and song["acousticness"] < 0.3:
        reasons.append(f"less acoustic than you prefer (acousticness {song['acousticness']})")

    explanation = "Because it " + ", and ".join(reasons) + "."
    return round(score, 4), explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(song, user_prefs)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
