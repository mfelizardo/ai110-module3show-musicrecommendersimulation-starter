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

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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



