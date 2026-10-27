# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

Name: **withTaste 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

**Answer:** 
- withTaste gives a ranked list of songs from a small sample catalog, based on a user's genre, mood, energy, and acoustic preferences. 
- It assumes the user already knows what they like and can describe it with those four preferences — it doesn't learn from listening history or feedback. 
- This is a classroom project built to practice and demonstrate how content-based recommendation logic works, not a tool meant for real-world use.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

**Answer:**

Think of the recommender as a judge that looks at every song in the catalog, one at a time, and asks four questions about how well it matches what the listener likes:

1. **Is it the same genre the listener favors?** If so, that's the biggest point boost — genre tends to say the most about how a song actually sounds.
2. **Does the mood match?** An exact mood match earns a solid bonus. If the mood isn't an exact match but is still in the same "family" of feeling (for example, "chill" and "relaxed" are both calm moods), the song still gets partial credit instead of being treated like a complete mismatch.
3. **Is the energy level close to what the listener wants?** This isn't about picking the highest-energy or lowest-energy song — it's about picking whichever song's energy sits closest to the listener's preferred level, whether that's calm or intense.
4. **Does the acoustic feel match the listener's taste?** If the listener prefers acoustic songs, more acoustic-sounding tracks score higher; if they prefer a more electronic sound, less-acoustic tracks score higher.

Every song picks up points from these four checks and ends up with one final number — its score. Once every song in the catalog has been judged this way, the system lines them all up from the highest score to the lowest and hands back the top few as the recommendations, along with a plain-English explanation of exactly which checks earned it those points.

**What changed from the starter logic:** the starter file was just a skeleton with placeholders — none of the scoring, loading, or ranking logic existed yet. We built the whole judging process described above, and along the way noticed that an early version of the mood check was too strict: it only rewarded an *exact* mood match and gave zero credit to moods that were basically synonyms (like "chill" and "relaxed"). We fixed that by grouping similar moods together so near-matches get partial credit instead of being penalized as if they were completely different.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

**Answer:**
- The catalog has **17 songs** total.
- It covers **14 genres** (pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop, classical, country, reggae, metal, folk, R&B) and **13 moods** (happy, chill, intense, relaxed, moody, focused, energetic, calm, nostalgic, romantic, angry, dreamy, sad).
- We started with 10 songs and added 7 more, picking genres/moods that weren't already covered (like hip hop, classical, and metal).
- Missing: real listening data (plays, skips, likes), lyrics or language, subgenres, and song popularity. Also, most genres only have 1 song each, so there's little room to compare songs within the same genre.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

**Answer:**
- Works best for users whose favorite genre has more than one song (like lofi), since the system has real options to rank against each other instead of just one automatic pick.
- The energy-closeness scoring captures the right idea: it rewards songs closest to the user's target energy, not just "high" or "low" energy, so it correctly handles users who want calm music just as well as users who want intense music.
- The mood-grouping fix works as intended: a song labeled "relaxed" still gets a fair amount of credit from a user who said "chill," instead of being treated as a total mismatch.
- In clear-cut tests (like "Chill Lofi" vs. "Deep Intense Rock"), the top results matched intuition well — completely different song types for completely different tastes, with no overlap.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Answer:**
- Features not considered: tempo, valence, danceability, and lyrics. They're stored in the data but don't affect the score.
- Underrepresented: 12 of the 14 genres have only 1 song each, so most genres have no real alternative to rank against.
- Overfitting example: in the "Extreme Target Energy" test, a user asked for a calm (energy 0.0) metal/angry song, but the system still recommended "Iron Reckoning" (energy 0.95) as #1 — the genre + mood bonus outweighed an almost total energy mismatch.
- Unintentional favoritism: users whose favorite genre has multiple songs (like lofi) get a real ranked comparison. Users whose favorite genre has only one song basically get that one song by default, regardless of fit.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

**Answer:**

I tested six user profiles against the 17-song catalog: three "normal" taste profiles and three adversarial/edge-case profiles designed to see if the scoring logic could be tricked or would produce surprising results.

**Normal profiles:**
- **High-Energy Pop** — `favorite_genre: "pop", favorite_mood: "happy", target_energy: 0.90, likes_acoustic: False`
- **Chill Lofi** — `favorite_genre: "lofi", favorite_mood: "chill", target_energy: 0.35, likes_acoustic: True`
- **Deep Intense Rock** — `favorite_genre: "rock", favorite_mood: "intense", target_energy: 0.90, likes_acoustic: False`

**Edge-case profiles:**
- **Conflicting preferences** — `favorite_genre: "R&B", favorite_mood: "sad", target_energy: 0.90, likes_acoustic: True` (a "sad" mood paired with a very high energy target — a combination that's emotionally contradictory)
- **Genre/mood not in the catalog at all** — `favorite_genre: "opera", favorite_mood: "euphoric", target_energy: 0.5, likes_acoustic: False`
- **Extreme target energy** — `favorite_genre: "metal", favorite_mood: "angry", target_energy: 0.0, likes_acoustic: False` (asking for a calm metal/angry song, when metal/angry songs in the catalog are all high-energy)

What I looked for: did the top result's genre/mood actually match the profile, did energy closeness behave symmetrically, and did a contradictory or nonsense profile crash, fail silently, or just produce a weird-but-explainable ranking.

**What surprised me:**
- Conflicting profile (R&B/sad + high energy): top result "Empty Hallways" had the *opposite* energy of what was asked (0.35 vs. 0.90) — the genre+mood bonus simply outweighed the energy mismatch.
- Nonexistent genre/mood (opera/euphoric): no error — it silently fell back to ranking by energy and acoustic fit alone, since nothing could earn a genre/mood bonus.
- Extreme target energy (metal/angry at 0.0): "Iron Reckoning" (energy 0.95) still won #1 — the furthest-possible energy mismatch, overridden by genre+mood.

**Profile comparisons:**

- **High-Energy Pop vs. Chill Lofi:** opposite requests, opposite results (fast/electronic vs. slow/acoustic) — correct behavior.
- **High-Energy Pop vs. Deep Intense Rock:** same energy level, different mood (happy vs. aggressive) — the system told them apart using mood, not just energy.
- **Chill Lofi vs. Deep Intense Rock:** zero overlap in top 5 — the most opposite pair we tested, as expected.
- **High-Energy Pop vs. Conflicting edge case:** Pop's winner matches on all 3 counts; the Conflicting winner only matches genre+mood and ignores the stated energy — same confidence, different reliability.
- **Chill Lofi vs. Genre/Mood-Not-in-Catalog edge case:** Lofi's results are genuinely similar; the made-up genre's results just happen to share an energy level — genre/mood never actually mattered for the second one.
- **Deep Intense Rock vs. Extreme Target Energy edge case:** Deep Intense Rock's request matches what the catalog has; the edge case doesn't, yet still gets a confident #1 pick anyway.

**Why does "Gym Hero" keep showing up for "Happy Pop"?** It's the right genre (pop) and has an energy level close to what a happy-pop fan wants — that's already enough points to rank high, even though its mood is "intense," not "happy." The system adds up several "pretty good" matches instead of requiring one perfect one, so a near-miss on mood can still win.

*Full terminal output for all six profiles is in `README.md` under "Sample Recommendation Output."*

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

**Answer:**
- Add more songs per genre so single-song genres stop auto-winning regardless of fit.
- Use tempo, valence, and danceability in scoring, not just energy and acousticness.
- Let users pick more than one favorite genre/mood instead of just one each.
- Warn the user when their genre/mood isn't in the catalog instead of silently ranking by energy alone.
- Add a bit of variety to the top 5 so results aren't always identical for the same profile.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

**Answer:**

The biggest thing I learned is that recommender systems are value-based, not objective. "Good recommendation" isn't a fact the system discovers, it's whatever the designer's chosen weights happen to produce. Our genre bonus, mood bonus, and energy formula weren't derived from any rule about what's "correct" — we just picked numbers, and those numbers decided every outcome from then on.

The clearest proof of this was the "Extreme Target Energy" test: a user asked for a calm, angry metal song (energy 0.0), and the system still confidently recommended the single most energetic song in the entire catalog (0.95) as its #1 pick. It wasn't a bug — the math worked exactly as designed. It just revealed that "genre and mood matter more than energy" was our assumption, not a universal truth, and the system had no way to know it was giving a bad answer.

That changed how I think about real apps like Spotify or YouTube: every "recommended for you" is the output of someone's weighting decisions, not a neutral read of what's objectively best for me. There's no reason their choices are any less arbitrary than ours — they're just better-tuned and tested on far more data.
