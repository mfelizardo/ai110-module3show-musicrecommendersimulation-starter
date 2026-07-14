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

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Real world music recommenders from services like Spotify and Youtube work by primarily using a blend of two different techniques: collaborative filtering and content-based filtering. Collaborative filtering involves identifying patterns across different users on the platform. It recommends songs to a user by finding other people with similar taste profiles based on similar song likes and then recommends songs the other people have listened that the user hasn't heard yet. The issue with only collaborative filtering however is that it is difficult to recommend completely brand new songs since no users have listened to it when it releases so the system can't identify a pattern between users. On the other hand, content-based filtering involves looking at the attributes of the songs themselves (genre, tempo, mood, energy, etc.) and recommends songs to a user with similar attributes. The weakness of using only this technique however is that the recommendations may seem too narrow, and fail to recommend songs that a user may actually like for reasons that are difficult to objectively measure. Spotify and other services combine both collaborative filtering and content-based filtering in their music recommendation algorithm in order to cover each other's weaknesses and strive to provide the best song recommendations to their users.

In my simple version of a music recommendation service, I will focus primarily on content-based filtering, mainly because as of now, there is no way for a user of this system to self-mark a song as "liked", which is needed in order to find patterns across multiple users. In my system, each `Song` carries a set of descriptive features — genre, mood, energy, tempo_bpm, valence, danceability, and acousticness — that capture both its category (genre/mood) and its audio character (the numeric features, mostly scaled 0–1). A `UserProfile` stores a compact taste profile: a favorite_genre, favorite_mood, a target_energy value, and a likes_acoustic flag. The `Recommender` scores each song by comparing it to the user's profile: genre and mood contribute points when they match the user's favorites, energy is scored by how close it is to the user's target_energy, and acousticness is scored against whether the user likes acoustic tracks. These individual feature scores are combined into a single weighted total for each song. To generate recommendations, every song in the catalog is scored this way, then sorted from highest to lowest score, and the top songs are returned as the final recommendation list.

Concretely, each song can earn up to 100 points: 25 points if its genre matches the user's favorite_genre, 25 points if its mood matches favorite_mood, up to 30 points scaled by how close its energy is to target_energy, and up to 20 points based on how well its acousticness aligns with the likes_acoustic flag. Genre and mood are weighted equally since both are strong, equally trustworthy taste signals, while energy gets the largest single weight because it's continuous and can reward near-misses rather than only rewarding exact matches. One bias I expect from this recipe is a skew toward whichever genre and mood tags are most common in the catalog: because genre and mood are scored as exact matches, users whose taste happens to line up with the dominant tags (like lofi/chill or pop/happy in this dataset) will consistently score higher and see more variety in their recommendations, while users with less common combinations get fewer strong matches.

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

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

### Stress Test: Diverse and Adversarial Profiles

`src/main.py` runs the recommender against three distinct "realistic" taste profiles plus four adversarial/edge-case profiles designed to try to break the scoring logic (conflicting preferences, a genre that doesn't exist in the catalog, an empty profile, and an out-of-range energy value). Run it yourself with `python -m src.main`. Actual terminal output below.

#### High-Energy Pop

```
=== Profile: High-Energy Pop ===
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'likes_acoustic': False}

Top recommendations:

Sunrise City - Score: 94.00
Because: genre match (pop) (+25.0); mood match (happy) (+25.0); energy closeness (+27.6); acousticness fit (+16.4)

Gym Hero - Score: 73.10
Because: genre match (pop) (+25.0); energy closeness (+29.1); acousticness fit (+19.0)

Rooftop Lights - Score: 63.80
Because: mood match (happy) (+25.0); energy closeness (+25.8); acousticness fit (+13.0)

Broken Curfew - Score: 47.80
Because: energy closeness (+28.8); acousticness fit (+19.0)

Storm Runner - Score: 47.70
Because: energy closeness (+29.7); acousticness fit (+18.0)
```

#### Chill Lofi

```
=== Profile: Chill Lofi ===
Preferences: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.3, 'likes_acoustic': True}

Top recommendations:

Library Rain - Score: 95.70
Because: genre match (lofi) (+25.0); mood match (chill) (+25.0); energy closeness (+28.5); acousticness fit (+17.2)

Midnight Coding - Score: 90.60
Because: genre match (lofi) (+25.0); mood match (chill) (+25.0); energy closeness (+26.4); acousticness fit (+14.2)

Spacewalk Thoughts - Score: 72.80
Because: mood match (chill) (+25.0); energy closeness (+29.4); acousticness fit (+18.4)

Focus Flow - Score: 67.60
Because: genre match (lofi) (+25.0); energy closeness (+27.0); acousticness fit (+15.6)

Autumn Requiem - Score: 47.50
Because: energy closeness (+28.5); acousticness fit (+19.0)
```

#### Deep Intense Rock

```
=== Profile: Deep Intense Rock ===
Preferences: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}

Top recommendations:

Storm Runner - Score: 97.70
Because: genre match (rock) (+25.0); mood match (intense) (+25.0); energy closeness (+29.7); acousticness fit (+18.0)

Gym Hero - Score: 73.10
Because: mood match (intense) (+25.0); energy closeness (+29.1); acousticness fit (+19.0)

Broken Curfew - Score: 47.80
Because: energy closeness (+28.8); acousticness fit (+19.0)

Skyline Pulse - Score: 47.70
Because: energy closeness (+28.5); acousticness fit (+19.2)

Iron Wraith - Score: 47.30
Because: energy closeness (+27.9); acousticness fit (+19.4)
```

#### Adversarial: Conflicting Signals (sad + high energy)

`mood="sad"` does not exist anywhere in `data/songs.csv` (the closest tag is `melancholic`), and pairing it with `energy=0.95` is internally contradictory (sad songs in the catalog tend to be low-energy). The scorer doesn't detect the contradiction — it just silently never awards the mood bonus and lets genre + energy + acoustic carry the ranking.

```
=== Profile: Conflicting Signals (sad + high energy) ===
Preferences: {'genre': 'rock', 'mood': 'sad', 'energy': 0.95, 'likes_acoustic': False}

Top recommendations:

Storm Runner - Score: 71.80
Because: genre match (rock) (+25.0); energy closeness (+28.8); acousticness fit (+18.0)

Skyline Pulse - Score: 49.20
Because: energy closeness (+30.0); acousticness fit (+19.2)

Iron Wraith - Score: 48.80
Because: energy closeness (+29.4); acousticness fit (+19.4)

Broken Curfew - Score: 48.70
Because: energy closeness (+29.7); acousticness fit (+19.0)

Gym Hero - Score: 48.40
Because: energy closeness (+29.4); acousticness fit (+19.0)
```

#### Adversarial: Unknown Genre (vaporwave)

`genre="vaporwave"` never appears in the catalog, so the genre bonus can never fire for anyone. The system degrades gracefully rather than erroring or returning an empty list — it just falls back to mood + energy + acoustic to rank songs.

```
=== Profile: Unknown Genre (vaporwave) ===
Preferences: {'genre': 'vaporwave', 'mood': 'chill', 'energy': 0.4, 'likes_acoustic': True}

Top recommendations:

Library Rain - Score: 70.70
Because: mood match (chill) (+25.0); energy closeness (+28.5); acousticness fit (+17.2)

Spacewalk Thoughts - Score: 69.80
Because: mood match (chill) (+25.0); energy closeness (+26.4); acousticness fit (+18.4)

Midnight Coding - Score: 68.60
Because: mood match (chill) (+25.0); energy closeness (+29.4); acousticness fit (+14.2)

Coffee Shop Stories - Score: 46.90
Because: energy closeness (+29.1); acousticness fit (+17.8)

Dust Road Home - Score: 45.80
Because: energy closeness (+29.4); acousticness fit (+16.4)
```

#### Adversarial: Empty Profile

With `{}`, every song scores exactly 0.00 ("no strong matches"), since no comparison keys are present. The interesting part is the tie-break behavior: `sorted()` is stable, so with every score tied, the top 5 come back in the exact order they appear in `data/songs.csv` (rows 1-5). That's a hidden default — a user who states zero preferences effectively gets "whatever is first in the catalog," not a random or popularity-based sample.

```
=== Profile: Empty Profile ===
Preferences: {}

Top recommendations:

Sunrise City - Score: 0.00
Because: no strong matches

Midnight Coding - Score: 0.00
Because: no strong matches

Storm Runner - Score: 0.00
Because: no strong matches

Library Rain - Score: 0.00
Because: no strong matches

Gym Hero - Score: 0.00
Because: no strong matches
```

#### Adversarial: Out-of-Range Energy

`energy=5.0` is far outside the expected 0-1 scale. `score_song` clamps `energy_diff = min(abs(song.energy - 5.0), 1.0)` to exactly `1.0` for every song (since the raw difference is always > 1), which zeroes out the entire 30-point energy term across the board ("energy closeness (+0.0)" everywhere). The clamp prevents a crash or a negative score, but it also means an out-of-range value silently removes an entire scoring dimension instead of raising a validation error — the recommender never tells the caller the input was invalid.

```
=== Profile: Out-of-Range Energy ===
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 5.0, 'likes_acoustic': False}

Top recommendations:

Sunrise City - Score: 66.40
Because: genre match (pop) (+25.0); mood match (happy) (+25.0); energy closeness (+0.0); acousticness fit (+16.4)

Gym Hero - Score: 44.00
Because: genre match (pop) (+25.0); energy closeness (+0.0); acousticness fit (+19.0)

Rooftop Lights - Score: 38.00
Because: mood match (happy) (+25.0); energy closeness (+0.0); acousticness fit (+13.0)

Iron Wraith - Score: 19.40
Because: energy closeness (+0.0); acousticness fit (+19.4)

Skyline Pulse - Score: 19.20
Because: energy closeness (+0.0); acousticness fit (+19.2)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

### Weight Shift: Double Energy, Halve Genre

**Change:** in `src/recommender.py`, `GENRE_WEIGHT` went from `25.0` to `12.5` and `ENERGY_WEIGHT` went from `30.0` to `60.0` (mood and acousticness weights unchanged). Max possible score rose from 100 to 117.5 — not an issue, since scores are only used for relative ranking, not treated as a percentage. Re-ran `python -m src.main` against all seven profiles (three "realistic" + four adversarial from the stress test above) and diffed the rankings against the original weights.

**What stayed the same:** for the three realistic profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock), the #1 and #2 recommendations never changed. When a song already had a strong genre + mood + energy match, it dominated regardless of how the weight was split between genre and energy.

**What changed — rankings actually flipped in the tail:**

- **Conflicting Signals profile:** Broken Curfew and Iron Wraith swapped places (rank 3 and 4). Before, Iron Wraith edged ahead by a slightly better acousticness fit (+19.4 vs +19.0). After doubling the energy weight, Broken Curfew's small energy-closeness edge (it's 0.01 closer to the target energy) got amplified enough to outweigh Iron Wraith's acoustic advantage.
- **Unknown Genre (vaporwave) profile:** Midnight Coding and Spacewalk Thoughts swapped (rank 2 and 3), and Focus Flow displaced Dust Road Home out of the top 5 entirely. Focus Flow's energy (0.40) is a near-exact match to the target (0.4), so doubling the energy weight pushed it from "not in the top 5" to rank 5.
- **Out-of-Range Energy profile:** since `energy=5.0` clamps every song's energy term to 0, this profile isolates genre + mood + acoustic. Gym Hero (a genuine pop/genre match) fell from rank 2 to rank 3, dropping *below* Rooftop Lights, which only has a mood match. Halving `GENRE_WEIGHT` directly caused this: Gym Hero's genre bonus dropped from +25 to +12.5, which was no longer enough to beat Rooftop Lights' mood + acoustic total.

The change didn't improve any profile's top pick; it mostly re-ordered close ties in ranks 3-5 by trading a categorical signal (genre match, all-or-nothing) for more influence from a continuous one (energy closeness). A user who cares about genre identity (e.g. "I only want pop songs") is now more easily outranked by a song from a different genre that merely happens to hit their target energy almost exactly. Energy-focused users benefit, genre-loyal users lose out — this is a tradeoff, not a strict improvement, and it reinforces that scoring weights encode a value judgment about which taste signal matters most.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

- lofi and chill are the most-repeated tags (3/19 songs each), so those users get more genuine matches, while 9 of 16 genres have only one song each.
- Energy and acousticness are scored the same regardless of genre, so unrelated-genre songs with a close numeric fit can bleed into a user's top 5 (seen in our stress test).
- `likes_acoustic` rewards acoustic *extremes*, not a stated preference strength — mid-range acousticness songs score mediocre either way.
- With only 19 songs, top-5 lists already cover a quarter of the catalog, leaving little room for novelty across different users.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



