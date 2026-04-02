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

---

### Context:

- First, some context on how irl streaming platforms predict what users will listen to next. They have two methods: Collaborative filtering, content-based filtering.
  - Collaborative filtering: If two users have similar taste histories, what one enjoys is a good prediction for the other.
    - Build a user-item matrix (rows = each user, columns = songs, values = plays/ratings).
    - Find users with similar behavior patterns (cosine similarity, matrix factorization).
    - Recommend said items that similar users liked.
    - Strengths: Discover surprising recommendations across genres.
    - Weaknesses: Cold start problem (new users/items have no history), popularity bias towards mainstream content.
  - Content-based filtering: Because a user liked a song with certain attributes, find items with similar attributes.
    - Extract features from items (tempo, key, danceability, genre, etc)/
    - Build profile of what user has engaged with.
    - Recommend items with high feature similarity to that profile.
    - Strengths: Work for new items immediately, explainable ("Because you liked this upbeat pop..."), no need for other users' data.
    - Weaknesses: Over-specialization, can't discover genuinely new content.

### My Planned System:

- Each Song is scored using five features: genre, mood, energy, tempo, and acousticness.
- The UserProfile stores a matching set of preferences: favorite_genre, favorite_mood, target_energy, target_tempo (added after listening to criticism from inline agent), and likes_acoustic.
  - The sample profile used for testing: genre = pop, mood = happy, target energy = 0.85, target tempo = 120 BPM, likes_acoustic = False.
- Scoring runs each song through score_song(), which computes a weighted sum capped at 1.0:
  - 0.40 × genre_score + 0.25 × mood_score + 0.20 × energy_score + 0.10 × tempo_score + 0.05 × acoustic_score
  - Genre and mood are binary matches (1.0 or 0.0). Energy and tempo use proximity to the user's target value. Acousticness applies a soft penalty if the user dislikes acoustic songs.
  - All songs are scored, sorted descending, and the top k are returned.
- This is content-based filtering — recommendations are derived entirely from song attributes matched against a single user's preferences, with no data from other users involved.
  - The trade-off is explainability and privacy at the cost of serendipity. That being said, given that we are composing a service similar to spotify and youtube, that doesn't necessarily mean the user is completely blocked off from expanding their scope to other genres, they can always search for themselves.
- **Potential Biases**:
  - Genre can be a finnicky filter to assign a high weight to. The idea though was that oftentimes people will assign certain vibes just based on genre, like rock and roll would be fast and encourage defiance, pop would be talking about daily life experiences.
    - A song in the wrong genre can never outscore a mediocre same-genre song, even if the other attributes are a perfect match.
  - Data has 6 pop songs and 6 happy songs out of 17 total.
  - Mood matching is either "fits the mood or doesn't".
- **Diagram**:
  - ![alt text](<Screenshot 2026-04-02 at 2.11.38 PM.jpg>)

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

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

- Limitations encountered during planning:
  - I had run my original user profile with inline chat and they had a criticsm that "intense rock" and "chill lofi" were differentiated for the wrong reasons (through target energy, not because it understood "intense" and "chill" as moods).
  - Mood is considered binary matching, a favorite mood of "happy" will consider both "intense" and "chill" as 0 equally.
  - Genre is too narrow. With "pop" as a target, a high-energy rock track would score worse than a mid-energy pop track. Just because the genre is different doesn't mean the user wouldn't have liked the "rock" example.
  - No tempo signal. Stuff like intense rock and chill lofi would be most cleanly separated by tempo (152 bpm and 72 bpm respectively).
  - Now I have refined profile to have target_tempo. It can now distinguish "high energy + fast tempo" from "high energy + slow tempo" and avoids the issue where energy alone conflates different types of intensity.

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---
- VibeCheck 3.6

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

- This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, energy and after consulting inline chat, now also checks **target_tempo**.


## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

```
