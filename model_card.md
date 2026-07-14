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

The system over-prioritizes lofi and chill music because those tags each appear on 3 of the 19 songs (15.8%), giving those users more genuinely-matching candidates, while 9 of 16 genres and several moods appear on only a single song, so a user with an underrepresented taste can only ever earn that bonus from one track in the whole catalog. Because energy and acousticness are scored identically regardless of genre, songs from unrelated genres with extreme energy or acousticness values can bleed into a user's top 5 alongside real genre matches — our stress test showed a metal track surfacing for a pop/high-energy profile and a classical track surfacing for a chill/lofi profile, purely on numeric closeness rather than taste relevance. The `likes_acoustic` flag also biases toward extremes rather than doing a flat true/false swing: the fit score is `acousticness` when `True` or `1 - acousticness` when `False`, so a song with mid-range acousticness (around 0.5) earns a mediocre score either way, meaning the system rewards songs at the acoustic extremes and gives users no way to express a preference for something in between. Combined with a catalog of only 19 songs — where a top-5 list already covers over a quarter of everything available — the system has little room to offer novelty and will recommend heavily overlapping songs to any users with even loosely similar profiles.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

### Profiles tested

I ran seven profiles through `python -m src.main` (see `src/main.py` and the README's "Stress Test" section for full output): three realistic tastes — **High-Energy Pop**, **Chill Lofi**, **Deep Intense Rock** — and four adversarial ones designed to try to trip up the scoring — **Conflicting Signals** (mood="sad", which doesn't exist in the catalog, paired with very high energy), **Unknown Genre** ("vaporwave", a genre that doesn't exist), **Empty Profile** (no preferences at all), and **Out-of-Range Energy** (`energy=5.0`, way outside the normal 0–1 scale). For each one I looked at whether the top 5 "made sense" given the stated taste, and whether any input — valid or broken — could make the system crash or return something nonsensical.

### Profile-to-profile comparisons

- **High-Energy Pop vs. Chill Lofi:** these two want opposite things (loud/happy/non-acoustic vs. soft/chill/acoustic), and their top 5 lists share zero songs. This makes sense, showing that the scorer actually separates opposite tastes instead of defaulting to the same "generically good" songs for everyone.
- **High-Energy Pop vs. Deep Intense Rock:** these ask for different genres and moods (pop/happy vs. rock/intense) but the *same* high energy (0.9) and the *same* dislike of acoustic songs. Their top 5s overlap on three songs (Gym Hero, Broken Curfew, Storm Runner). That also makes sense because energy and acousticness are scored the same way no matter the genre, so any song that's loud and electric will do well for both a "pop fan" and a "rock fan" as long as they both want high energy.
- **Deep Intense Rock vs. Conflicting Signals:** both want genre=rock and very high energy, but Conflicting Signals asks for mood="sad" instead of a tag that makes sense for a rock lover like "intense." The exact same 5 songs show up in both lists, just reshuffled — Gym Hero drops from rank 2 to rank 5 once it loses its 25-point mood bonus (it's tagged "intense," not "sad"). This shows the impact of the mood field: take it away and a song can fall several spots even though nothing else about it changed.
- **Chill Lofi vs. Unknown Genre (vaporwave):** vaporwave keeps mood=chill and likes_acoustic=True but sets a genre that doesn't exist, so the genre bonus is never awarded. The top 3 songs are identical to Chill Lofi's (just re-ordered). In this catalog, the songs tagged "chill" also happen to be strongly acoustic, and mood and acousticness alone can almost reconstruct what genre matching would have done. Ranks 4–5 do change, though (Focus Flow/Autumn Requiem swapped for Coffee Shop Stories/Dust Road Home), since without a genre anchor, other acoustic chill-ish songs from unrelated genres get higher scores.
- **High-Energy Pop vs. Out-of-Range Energy:** identical preferences except `energy=5.0` instead of `0.9`. The top 3 (Sunrise City, Gym Hero, Rooftop Lights) stay in the same order — genre and mood matches still carry them. But ranks 4–5 change completely: Broken Curfew and Storm Runner (which relied on a good *energy* score) drop out, replaced by Iron Wraith and Skyline Pulse (which have almost zero acousticness and win purely on the acoustic-fit term once energy contributes nothing). This shows how the energy calculation just quietly removes itself if a user profile has an out-of-range value, leaving the other three categories to determine the song rankings.
- **Empty Profile vs. everything else:** with no preferences, every song ties at a score of 0, and the "top 5" is just the first 5 rows of `data/songs.csv` in file order (Sunrise City, Midnight Coding, Storm Runner, Library Rain, Gym Hero). It isn't a popularity list or a random sample — it's an artifact of how Python's stable sort breaks ties. A real product would probably want a different fallback (e.g., trending songs) for users who haven't told it anything yet.

### What surprised me

The biggest surprise was how often **the same handful of songs kept reappearing across very different profiles** because they sit at an extreme on one or two numeric dimensions (very high energy, or near-zero/near-one acousticness). One example is: **"Gym Hero" keeps showing up for people who just say they want "Happy Pop,"** even though Gym Hero's mood tag is actually "intense," not "happy." This is because Gym Hero is genuinely a pop song (genre match, +25 points), it's about as high-energy as a song can get (target was 0.9, Gym Hero is 0.93 — almost a perfect match, +29 points), and it's almost completely non-acoustic (which is also what a "Happy Pop" fan who dislikes acoustic songs wants, +19 points). Even though it misses the "happy" mood entirely (losing 25 possible points), it still racks up enough points from the other three ingredients to land at #2. In other words, the system doesn't require a song to match *every* stated preference — it just needs to be strong enough on enough of them, and a song that's an extreme, unambiguous example of "loud, poppy, and electronic" will keep floating to the top for anyone who wants loud, poppy, and electronic, whether or not its mood label is technically the one they asked for.

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
