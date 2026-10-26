# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works
My understanding of how real-world recomendations work: 
Real world reccomendations use both collaborative filtering and content-based filter to recommend songs to
users. Songs have weights and values to decide which song to suggest to the user based on the user's data. It is either determined by other user's who have similar preferences or by songs that have similar based values to the song the user is currently listening to.

My version will use content-based filtering since there isn't multiple user data available to compare against. It will score songs by how closely their features match a target (the seed song or user profile) and then rank them in that order. 

Explain your design in plain language.
Every song has at least 3 attributes: Genre, Mood, and energy levl. 
The user has a simple profile for their tailored taste. 


To recommend songs, the system goes through every song in the catalog and gives it points based on how well it matches the user:

- Same genre as the user's favorite? Big bonus points.
- Same mood as the user's favorite? Smaller bonus points — and if the mood isn't an exact match but is still similar (e.g., "chill" and "relaxed" are both calm moods), it gets partial credit instead of none, so close-but-not-exact moods aren't penalized as if they were totally different.
- Energy level close to what the user wants? The closer it is, the more points — being too high or too low both lose points equally.
- Acoustic sound matches the user's preference? Small bonus or small penalty, depending on whether they like acoustic songs.

Once the scoring is calculated, the system sorts the scores from highest to lowest and returns the top few as recommendations along with a short explanation. 


Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
   Answer: our scoring design actively uses genre, mood, energy, and acousticness to compute recommendations — tempo_bpm, valence, and danceability are stored on each song but not currently part of the scoring formula, since the UserProfile doesn't track target preferences for them.

- What information does your `UserProfile` store
  Answer:  
- favorite_genre — the genre the user prefers (e.g., "pop")
- favorite_mood — the mood the user prefers (e.g., "happy")
- target_energy (0–1) — the energy level the user wants songs to be close to
- likes_acoustic (bool) — whether the user prefers more acoustic-sounding songs or not

- How does your `Recommender` compute a score for each song
Answer: the Recommender scores each song by comparing it against the user's profile and adding up points from four rules:

1. Genre match — +3 points if the song's genre equals the user's favorite_genre.
2. Mood match — +2 points if the song's mood exactly equals the user's favorite_mood, or +1 point if it's not exact but still falls in the same mood group (moods are grouped into "upbeat," "calm," "aggressive," and "somber" clusters so synonyms like "chill" and "relaxed" aren't treated as a total mismatch).
3. Energy closeness — 2 × (1 - |song.energy - target_energy|). The closer the song's energy is to the user's target_energy, the higher this score — being too high or too low both lose points equally, since it's based on distance, not magnitude.
4. Acousticness preference — song.acousticness (as a bonus, up to +1) if likes_acoustic is True, or (1 - song.acousticness) if False — so the system rewards matching the user's actual preference in either direction, not just "more acoustic is always better."

score = genre_bonus + mood_bonus + 2*(1 - |energy - target_energy|) + acoustic_adjustment
Higher score means a better match to the user's taste profile.

- How do you choose which songs to recommend
answer: We choose songs according to the Ranking Rule. It will score every song, sort the songs from highest to lowest, return k amount of songs. If there's a tie, it will prefer the energy that's closer to target_energy. 

### Potential Biases in This Design

- **Genre dominance** — genre is weighted highest (+3), so a song that's the "wrong" genre can rank low even if its mood, energy, and acousticness are a near-perfect match. The system is biased toward genre labels over how a song actually sounds or feels.
- **Mood grouping is a subjective judgment call** — the "upbeat / calm / aggressive / somber" clusters were manually defined by us, not derived from data. A different designer could group moods differently, which would quietly change which songs get partial credit.
- **Binary acoustic preference** — `likes_acoustic` is a single True/False flag, so it can't represent a user who's mostly okay with electronic music but still enjoys some acoustic tracks — real taste is rarely all-or-nothing.
- **Narrow profile = narrow taste** — a `UserProfile` represents exactly one favorite genre and one favorite mood, so the system can't recommend well for someone with multiple, varied tastes (e.g., a user who likes both lofi-chill and upbeat pop).
- **Small, hand-picked catalog** — all scoring happens over ~17 songs we wrote ourselves, so the weighting choices (genre +3, mood +2, etc.) haven't been tested against a large or diverse real-world dataset and may not generalize.
- **No popularity or social signal** — since this is content-based only (no collaborative filtering), the system can't learn from what similar users liked, so it will never surface a song purely because "people like you enjoyed it."

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

**Default profile** (`favorite_genre: "pop", favorite_mood: "happy", target_energy: 0.8, likes_acoustic: False`, from `src/main.py`):

```
Loaded songs: 17

================== Top 5 Recommendations ===================

1. Sunrise City  (Score: 7.78)
     - genre match: pop (+3.0)
     - mood match: happy (+2.0)
     - energy closeness: 0.82 vs target 0.80 (+1.96)
     - acoustic fit: 0.18 matches non-acoustic preference (+0.82)

2. Gym Hero  (Score: 5.69)
     - genre match: pop (+3.0)
     - energy closeness: 0.93 vs target 0.80 (+1.74)
     - acoustic fit: 0.05 matches non-acoustic preference (+0.95)

3. Rooftop Lights  (Score: 4.57)
     - mood match: happy (+2.0)
     - energy closeness: 0.76 vs target 0.80 (+1.92)
     - acoustic fit: 0.35 matches non-acoustic preference (+0.65)

4. Street Pulse  (Score: 3.76)
     - mood group match: energetic ~ happy (+1.0)
     - energy closeness: 0.88 vs target 0.80 (+1.84)
     - acoustic fit: 0.08 matches non-acoustic preference (+0.92)

5. Island Sway  (Score: 3.10)
     - mood group match: romantic ~ happy (+1.0)
     - energy closeness: 0.55 vs target 0.80 (+1.50)
     - acoustic fit: 0.40 matches non-acoustic preference (+0.60)
```

See `model_card.md` Section 7 (Evaluation) for the full write-up comparing this and five other test profiles — three "normal" taste profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) and three adversarial edge cases (conflicting mood/energy, a genre/mood not in the catalog, and an extreme target energy). The additional profiles' raw outputs below:

```
======================================================================
PROFILE: High-Energy Pop
user_prefs = {'favorite_genre': 'pop', 'favorite_mood': 'happy', 'target_energy': 0.9, 'likes_acoustic': False}
======================================================================
1. Sunrise City (pop/happy)  (Score: 7.66)
     - genre match: pop (+3.0)
     - mood match: happy (+2.0)
     - energy closeness: 0.82 vs target 0.90 (+1.84)
     - acoustic fit: 0.18 matches non-acoustic preference (+0.82)
2. Gym Hero (pop/intense)  (Score: 5.89)
     - genre match: pop (+3.0)
     - energy closeness: 0.93 vs target 0.90 (+1.94)
     - acoustic fit: 0.05 matches non-acoustic preference (+0.95)
3. Rooftop Lights (indie pop/happy)  (Score: 4.37)
     - mood match: happy (+2.0)
     - energy closeness: 0.76 vs target 0.90 (+1.72)
     - acoustic fit: 0.35 matches non-acoustic preference (+0.65)
4. Street Pulse (hip hop/energetic)  (Score: 3.88)
     - mood group match: energetic ~ happy (+1.0)
     - energy closeness: 0.88 vs target 0.90 (+1.96)
     - acoustic fit: 0.08 matches non-acoustic preference (+0.92)
5. Island Sway (reggae/romantic)  (Score: 2.90)
     - mood group match: romantic ~ happy (+1.0)
     - energy closeness: 0.55 vs target 0.90 (+1.30)
     - acoustic fit: 0.40 matches non-acoustic preference (+0.60)
```

```
======================================================================
PROFILE: Chill Lofi
user_prefs = {'favorite_genre': 'lofi', 'favorite_mood': 'chill', 'target_energy': 0.35, 'likes_acoustic': True}
======================================================================
1. Library Rain (lofi/chill)  (Score: 7.86)
     - genre match: lofi (+3.0)
     - mood match: chill (+2.0)
     - energy closeness: 0.35 vs target 0.35 (+2.00)
     - acoustic fit: 0.86 matches acoustic preference (+0.86)
2. Midnight Coding (lofi/chill)  (Score: 7.57)
     - genre match: lofi (+3.0)
     - mood match: chill (+2.0)
     - energy closeness: 0.42 vs target 0.35 (+1.86)
     - acoustic fit: 0.71 matches acoustic preference (+0.71)
3. Focus Flow (lofi/focused)  (Score: 6.68)
     - genre match: lofi (+3.0)
     - mood group match: focused ~ chill (+1.0)
     - energy closeness: 0.40 vs target 0.35 (+1.90)
     - acoustic fit: 0.78 matches acoustic preference (+0.78)
4. Spacewalk Thoughts (ambient/chill)  (Score: 4.78)
     - mood match: chill (+2.0)
     - energy closeness: 0.28 vs target 0.35 (+1.86)
     - acoustic fit: 0.92 matches acoustic preference (+0.92)
5. Coffee Shop Stories (jazz/relaxed)  (Score: 3.85)
     - mood group match: relaxed ~ chill (+1.0)
     - energy closeness: 0.37 vs target 0.35 (+1.96)
     - acoustic fit: 0.89 matches acoustic preference (+0.89)
```

```
======================================================================
PROFILE: Deep Intense Rock
user_prefs = {'favorite_genre': 'rock', 'favorite_mood': 'intense', 'target_energy': 0.9, 'likes_acoustic': False}
======================================================================
1. Storm Runner (rock/intense)  (Score: 7.88)
     - genre match: rock (+3.0)
     - mood match: intense (+2.0)
     - energy closeness: 0.91 vs target 0.90 (+1.98)
     - acoustic fit: 0.10 matches non-acoustic preference (+0.90)
2. Gym Hero (pop/intense)  (Score: 4.89)
     - mood match: intense (+2.0)
     - energy closeness: 0.93 vs target 0.90 (+1.94)
     - acoustic fit: 0.05 matches non-acoustic preference (+0.95)
3. Iron Reckoning (metal/angry)  (Score: 3.87)
     - mood group match: angry ~ intense (+1.0)
     - energy closeness: 0.95 vs target 0.90 (+1.90)
     - acoustic fit: 0.03 matches non-acoustic preference (+0.97)
4. Street Pulse (hip hop/energetic)  (Score: 2.88)
     - energy closeness: 0.88 vs target 0.90 (+1.96)
     - acoustic fit: 0.08 matches non-acoustic preference (+0.92)
5. Sunrise City (pop/happy)  (Score: 2.66)
     - energy closeness: 0.82 vs target 0.90 (+1.84)
     - acoustic fit: 0.18 matches non-acoustic preference (+0.82)
```

```
======================================================================
PROFILE: Edge Case — Conflicting (High Energy + Sad Mood)
user_prefs = {'favorite_genre': 'R&B', 'favorite_mood': 'sad', 'target_energy': 0.9, 'likes_acoustic': True}
======================================================================
1. Empty Hallways (R&B/sad)  (Score: 6.35)
     - genre match: R&B (+3.0)
     - mood match: sad (+2.0)
     - energy closeness: 0.35 vs target 0.90 (+0.90)
     - acoustic fit: 0.45 matches acoustic preference (+0.45)
2. Night Drive Loop (synthwave/moody)  (Score: 2.92)
     - mood group match: moody ~ sad (+1.0)
     - energy closeness: 0.75 vs target 0.90 (+1.70)
     - acoustic fit: 0.22 matches acoustic preference (+0.22)
3. Dusty Backroads (country/nostalgic)  (Score: 2.90)
     - mood group match: nostalgic ~ sad (+1.0)
     - energy closeness: 0.50 vs target 0.90 (+1.20)
     - acoustic fit: 0.70 matches acoustic preference (+0.70)
4. Storm Runner (rock/intense)  (Score: 2.08)
     - energy closeness: 0.91 vs target 0.90 (+1.98)
     - acoustic fit: 0.10 matches acoustic preference (+0.10)
5. Rooftop Lights (indie pop/happy)  (Score: 2.07)
     - energy closeness: 0.76 vs target 0.90 (+1.72)
     - acoustic fit: 0.35 matches acoustic preference (+0.35)
```

```
======================================================================
PROFILE: Edge Case — Genre/Mood Not In Catalog
user_prefs = {'favorite_genre': 'opera', 'favorite_mood': 'euphoric', 'target_energy': 0.5, 'likes_acoustic': False}
======================================================================
1. Island Sway (reggae/romantic)  (Score: 2.50)
     - energy closeness: 0.55 vs target 0.50 (+1.90)
     - acoustic fit: 0.40 matches non-acoustic preference (+0.60)
2. Dusty Backroads (country/nostalgic)  (Score: 2.30)
     - energy closeness: 0.50 vs target 0.50 (+2.00)
     - acoustic fit: 0.70 matches non-acoustic preference (+0.30)
3. Night Drive Loop (synthwave/moody)  (Score: 2.28)
     - energy closeness: 0.75 vs target 0.50 (+1.50)
     - acoustic fit: 0.22 matches non-acoustic preference (+0.78)
4. Empty Hallways (R&B/sad)  (Score: 2.25)
     - energy closeness: 0.35 vs target 0.50 (+1.70)
     - acoustic fit: 0.45 matches non-acoustic preference (+0.55)
5. Sunrise City (pop/happy)  (Score: 2.18)
     - energy closeness: 0.82 vs target 0.50 (+1.36)
     - acoustic fit: 0.18 matches non-acoustic preference (+0.82)
```

```
======================================================================
PROFILE: Edge Case — Extreme Target Energy (0.0)
user_prefs = {'favorite_genre': 'metal', 'favorite_mood': 'angry', 'target_energy': 0.0, 'likes_acoustic': False}
======================================================================
1. Iron Reckoning (metal/angry)  (Score: 6.07)
     - genre match: metal (+3.0)
     - mood match: angry (+2.0)
     - energy closeness: 0.95 vs target 0.00 (+0.10)
     - acoustic fit: 0.03 matches non-acoustic preference (+0.97)
2. Gym Hero (pop/intense)  (Score: 2.09)
     - mood group match: intense ~ angry (+1.0)
     - energy closeness: 0.93 vs target 0.00 (+0.14)
     - acoustic fit: 0.05 matches non-acoustic preference (+0.95)
3. Storm Runner (rock/intense)  (Score: 2.08)
     - mood group match: intense ~ angry (+1.0)
     - energy closeness: 0.91 vs target 0.00 (+0.18)
     - acoustic fit: 0.10 matches non-acoustic preference (+0.90)
4. Empty Hallways (R&B/sad)  (Score: 1.85)
     - energy closeness: 0.35 vs target 0.00 (+1.30)
     - acoustic fit: 0.45 matches non-acoustic preference (+0.55)
5. Moonlight Reverie (classical/calm)  (Score: 1.65)
     - energy closeness: 0.20 vs target 0.00 (+1.60)
     - acoustic fit: 0.95 matches non-acoustic preference (+0.05)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

**Answer — Weight Shift experiment:** I temporarily changed `GENRE_MATCH_BONUS` from `3.0` to `1.5` (halved) and `ENERGY_WEIGHT` from `2.0` to `4.0` (doubled) in `recommender.py`, then re-ran the default profile (`pop`/`happy`/`target_energy: 0.8`).

The math stayed valid — every song's score still computed correctly as `genre_bonus + mood_bonus + 4*(1 - |energy diff|) + acoustic_fit`, no errors or out-of-range values, and both existing tests still passed.

The ranking **did** change: "Rooftop Lights" (mood match + good energy, but genre `"indie pop"` doesn't exactly match `"pop"`) jumped from #3 to #2, overtaking "Gym Hero" (genre match + near-perfect energy, but no mood match at all), which dropped from #2 to #3. The #1 song (Sunrise City) stayed #1 either way, since it's the only song matching on every rule.

**Was it more accurate, or just different?** Just different — neither weighting is objectively "more correct." Doubling energy's weight makes the system lean harder toward "how intense does this song feel" and away from "is this literally the same genre," which is a reasonable choice for a listener who cares more about vibe than genre labels, but there's no ground-truth answer in this dataset to say one is actually better. It demonstrates that our scoring is **sensitive** to these weights — a fairly small change to two constants was enough to flip the #2/#3 order — which is itself a useful thing to know about the system's behavior. I reverted the weights back to the original 3.0/2.0 after the experiment.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
