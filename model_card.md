# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

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

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Answer:** The system over-prioritizes genre and mood exact-matches over energy fit, because 12 of the catalog's 14 genres contain only one song each. This means a user whose favorite genre is, say, "metal" has exactly one possible genre match, and that song's +3 genre bonus plus mood bonus is large enough to overpower an almost total energy mismatch. I confirmed this in the "Extreme Target Energy" edge-case test: a user wanting a calm (energy 0.0) metal/angry song was still recommended "Iron Reckoning" (energy 0.95) as the #1 result, even though its energy was about as wrong as possible. The weakness isn't a bug in the math — it's that a tiny, single-example-per-genre catalog combined with heavy genre/mood weighting leaves the system no real alternative to offer, so it confidently recommends a poor energy fit rather than honestly reflecting that no good match exists.

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

What I looked for: whether the top result's genre/mood actually matched the profile, whether energy closeness behaved symmetrically, and whether a nonsensical or self-contradictory profile would crash, silently fail, or quietly produce a weird-but-explainable ranking.

**What surprised me:**
- In the **conflicting profile** (R&B/sad + high energy), the system still ranked "Empty Hallways" (R&B/sad, energy 0.35) #1 even though its energy is the *opposite* of the requested 0.90 — the genre+mood bonus (+5) simply outweighed the energy penalty. This confirms the bias we flagged earlier: genre/mood dominance can override a legitimate, strongly-stated numeric preference.
- In the **nonexistent genre/mood profile** (opera/euphoric), the system didn't error or return nothing — it just silently fell back to ranking purely by energy closeness and acoustic fit, since no song could ever earn the genre or mood bonus. The recommender has no way to signal "I don't recognize this genre" — it just quietly ignores it.
- In the **extreme target energy profile** (metal/angry at energy 0.0), "Iron Reckoning" won with a score of 6.07 despite its energy (0.95) being as far as possible from the target (0.0) — again, the genre+mood bonus alone was enough to overcome an almost-total energy mismatch. This is the clearest evidence that our weighting lets a strong categorical match overpower a contradictory numeric preference.

**Comparing profiles against each other (in plain language):**

- **High-Energy Pop vs. Chill Lofi:** these two profiles share almost nothing — Chill Lofi's winner ("Library Rain") is a slow, mellow, mostly-acoustic song, while High-Energy Pop's winner ("Sunrise City") is a fast, electronic-sounding, upbeat song. That makes sense: the two people asked for opposite things — one wants calm background music, the other wants something loud and happy — so a good recommender *should* send them in completely different directions, and ours does.

- **High-Energy Pop vs. Deep Intense Rock:** both of these listeners want high-energy music (around 0.90), but Pop's winner is cheerful ("Sunrise City," a happy song) while Rock's winner is aggressive ("Storm Runner," an intense song). This makes sense too — "high energy" just means "a lot of intensity," it doesn't say *what kind* of feeling that intensity carries. Our system correctly tells those two apart using the mood, not just the energy number.

- **Chill Lofi vs. Deep Intense Rock:** these are the two most opposite profiles we tested, and the results show it — Lofi's whole top 5 are soft, acoustic, low-energy songs, while Rock's whole top 5 are loud, electronic-sounding, high-energy songs. There's zero overlap in the top 5 between them. That's exactly what you'd want: a system that can't tell a chill listener from an intense-rock listener wouldn't be very useful.

- **High-Energy Pop vs. the "Conflicting" edge case:** the normal Pop profile and the Conflicting profile (R&B fan who says they want "sad" music at "very high energy") both got a confident #1 answer — but the Conflicting one shouldn't feel as trustworthy. The Pop profile's winner matches on every count (genre, mood, *and* energy), while the Conflicting profile's winner only wins because it matches genre and mood — its energy is actually the opposite of what was asked for. Side by side, this shows the system can't tell the difference between "a confident, well-earned answer" and "a confident answer that's quietly ignoring half of what you said."

- **Chill Lofi vs. the "Genre/Mood Not in Catalog" edge case:** Chill Lofi gets songs that are genuinely similar to "lofi" and "chill" in every sense. The made-up "opera/euphoric" profile gets songs that happen to have the right energy level, but have nothing to do with opera or euphoria — the system just quietly swapped in "closest energy" as a replacement for "closest vibe" without saying so. Comparing them side by side shows how much weaker an answer looks once you know genre and mood never actually mattered for the second one.

- **Deep Intense Rock vs. the "Extreme Target Energy" edge case:** both profiles ask for "rock-like, intense" music, but the second one specifically asks for *calm* intensity (energy 0.0), which doesn't really exist for that genre in our data. Deep Intense Rock gets a great answer because a calm-ish intense rock song doesn't need to exist — the request and the catalog line up. The edge case doesn't: the system still hands back a confident #1 pick ("Iron Reckoning"), but it's the *most* energetic song in the whole catalog, the literal opposite of what was asked. Comparing the two shows that a strong genre/mood match can mask a request the catalog can't actually satisfy.

**Why does "Gym Hero" keep showing up when someone just wants "Happy Pop"?**

Imagine you tell a music app "I want something happy and poppy," and it keeps suggesting a gym workout anthem that's really more "pumped up" than "happy." Here's why that happens in plain terms: our system gives big bonus points for matching the *genre* (is it pop? yes) and separately checks if the *mood* matches exactly (is it labeled "happy"? no, it's labeled "intense"). Even without that mood bonus, "Gym Hero" still racks up a lot of points because it's a pop song (big bonus) and its energy level happens to be close to what a "happy pop" fan typically wants (another decent chunk of points). So it's not that the system thinks "intense" and "happy" are the same thing — it's that being the right *genre* and having the right *energy* is already enough points to land in the top few, even when the mood label doesn't actually match. In short: the system is good at spotting "this sounds like the right kind of song" but can still recommend something that doesn't quite feel right, because it's adding up several "pretty good" matches instead of requiring one "perfect" match.

*Full terminal output for each of the six profiles tested above is in `README.md` under "Sample Recommendation Output"*

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
