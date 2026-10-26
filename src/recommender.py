import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Moods that feel similar get grouped together so songs aren't penalized
# for a near-synonym label mismatch (e.g. "chill" vs "relaxed").
MOOD_GROUPS = {
    "happy": "upbeat",
    "energetic": "upbeat",
    "romantic": "upbeat",
    "chill": "calm",
    "relaxed": "calm",
    "calm": "calm",
    "focused": "calm",
    "dreamy": "calm",
    "intense": "aggressive",
    "angry": "aggressive",
    "moody": "somber",
    "sad": "somber",
    "nostalgic": "somber",
}

GENRE_MATCH_BONUS = 3.0
MOOD_MATCH_BONUS = 2.0
MOOD_GROUP_BONUS = 1.0
ENERGY_WEIGHT = 2.0


def _mood_score(song_mood: str, favorite_mood: str) -> float:
    """Returns the mood bonus: full credit for an exact match, partial credit for the same mood group, else 0."""
    if song_mood == favorite_mood:
        return MOOD_MATCH_BONUS
    if song_mood in MOOD_GROUPS and MOOD_GROUPS.get(song_mood) == MOOD_GROUPS.get(favorite_mood):
        return MOOD_GROUP_BONUS
    return 0.0


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

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Scores a single song against the user's profile, returning the total score and a reason per rule."""
        reasons: List[str] = []
        score = 0.0

        if song.genre == user.favorite_genre:
            score += GENRE_MATCH_BONUS
            reasons.append(f"genre match: {user.favorite_genre} (+{GENRE_MATCH_BONUS:.1f})")

        mood_points = _mood_score(song.mood, user.favorite_mood)
        if mood_points == MOOD_MATCH_BONUS:
            score += mood_points
            reasons.append(f"mood match: {user.favorite_mood} (+{mood_points:.1f})")
        elif mood_points == MOOD_GROUP_BONUS:
            score += mood_points
            reasons.append(f"mood group match: {song.mood} ~ {user.favorite_mood} (+{mood_points:.1f})")

        energy_closeness = 1 - abs(song.energy - user.target_energy)
        energy_points = ENERGY_WEIGHT * energy_closeness
        score += energy_points
        reasons.append(
            f"energy closeness: {song.energy:.2f} vs target {user.target_energy:.2f} (+{energy_points:.2f})"
        )

        acoustic_fit = song.acousticness if user.likes_acoustic else (1 - song.acousticness)
        score += acoustic_fit
        preference = "acoustic" if user.likes_acoustic else "non-acoustic"
        reasons.append(f"acoustic fit: {song.acousticness:.2f} matches {preference} preference (+{acoustic_fit:.2f})")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Scores every song against the user's profile and returns the top k, highest score first."""
        scored = [(self._score(user, song)[0], song) for song in self.songs]
        scored.sort(key=lambda item: (item[0], -abs(item[1].energy - user.target_energy)), reverse=True)
        return [song for (_, song) in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable sentence explaining why this song scored the way it did for the user."""
        _, reasons = self._score(user, song)
        return "Because " + "; ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    reasons: List[str] = []
    score = 0.0

    favorite_genre = user_prefs.get("favorite_genre")
    favorite_mood = user_prefs.get("favorite_mood")
    target_energy = user_prefs.get("target_energy", 0.5)
    likes_acoustic = user_prefs.get("likes_acoustic")

    if song.get("genre") == favorite_genre:
        score += GENRE_MATCH_BONUS
        reasons.append(f"genre match: {favorite_genre} (+{GENRE_MATCH_BONUS:.1f})")

    mood_points = _mood_score(song.get("mood", ""), favorite_mood or "")
    if mood_points == MOOD_MATCH_BONUS:
        score += mood_points
        reasons.append(f"mood match: {favorite_mood} (+{mood_points:.1f})")
    elif mood_points == MOOD_GROUP_BONUS:
        score += mood_points
        reasons.append(f"mood group match: {song.get('mood')} ~ {favorite_mood} (+{mood_points:.1f})")

    energy = float(song.get("energy", 0.0))
    energy_closeness = 1 - abs(energy - target_energy)
    energy_points = ENERGY_WEIGHT * energy_closeness
    score += energy_points
    reasons.append(f"energy closeness: {energy:.2f} vs target {target_energy:.2f} (+{energy_points:.2f})")

    acousticness = float(song.get("acousticness", 0.0))
    if likes_acoustic is None:
        acoustic_fit = 0.5
        reasons.append(f"acoustic fit: {acousticness:.2f}, no preference set (+{acoustic_fit:.2f})")
    else:
        acoustic_fit = acousticness if likes_acoustic else (1 - acousticness)
        preference = "acoustic" if likes_acoustic else "non-acoustic"
        reasons.append(f"acoustic fit: {acousticness:.2f} matches {preference} preference (+{acoustic_fit:.2f})")
    score += acoustic_fit

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    target_energy = user_prefs.get("target_energy", 0.5)
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) + "."
        scored.append((song, score, explanation))

    scored.sort(
        key=lambda item: (item[1], -abs(float(item[0].get("energy", 0.0)) - target_energy)),
        reverse=True,
    )
    return scored[:k]
