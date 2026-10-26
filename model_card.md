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

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
