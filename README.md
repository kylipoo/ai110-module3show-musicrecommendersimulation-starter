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
- Scoring runs each song through score_song(), which computes a weighted sum capped at 1.0 (represents a percentage of how close it matches the desired result):
  - 0.40 × genre_score + 0.25 × mood_score + 0.20 × energy_score + 0.10 × tempo_score + 0.05 × acoustic_score
  - Genre and mood are binary matches (1.0 or 0.0). Energy and tempo use proximity to the user's target value. Acousticness applies a soft penalty if the user dislikes acoustic songs.
  - Tempo score and acoustic score will need some additional calculation to convert in terms of percentage match.
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

- My system returned different song recommendations depending on the user profile's preferences. This has the explanation of checking first and foremost if the genre and the mood changed, as they are the highest weighed elements of the recipe.
- When I tried a user profile that had conflicting attributes (Lo-fi rager), the results returned were very low-scored, since genre is presently a 1 or nothing score, yet at the same time the target energy of that profile doesn't match any of the Lo-fi results.
  - HOWEVER, when I tried a different formula where the energy was given more weight (doubled from 0.2 to 0.4), the same results were scored higher because energy is a more numeric attribute instead of a binary 1 or 0 to see if it matches exactly.
- I added target tempo, which gave a more precise means of distinguishing profiles like intense rock or chill lofi.

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

- Limitations encountered during planning:
  - I had run my original user profile with inline chat and they had a criticism that "intense rock" and "chill lofi" were differentiated for the wrong reasons (through target energy, not because it understood "intense" and "chill" as moods).
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

- Building this recommender showed me that turning data into predictions is really about encoding assumptions and discerning patterns. Every weight in score_song is a judgement call: The system scores songs by weighing numeric attributes such as energy or tempo against a user's stated preferences, then ranks by closeness. That sounds objective, but then the weights are the deciding factor in what "close enough" means. Doubling the energy from 0.2->0.4 completely changed song scores and which ones surfaced, even for users where said genre was top priority. The prediction isn't from the data, it's from choices basked into the formula.
- The bias risk follows directly from that. If the catalog underrepresents certain genres or moods, users with those preferences get worse results through no fault of the algorithm — it's just working with incomplete data. The "Lofi Rager" profile in the code is a clear example: a user who wants intense, high-energy lofi gets broken recommendations because that niche doesn't exist in the dataset. In a real product, that pattern would fall hardest on listeners with niche or non-mainstream tastes, while users who prefer well-catalogued genres like pop consistently get better results. The system appears fair because it applies the same formula to everyone, but equal treatment of unequal data still produces unequal outcomes.

## 7. `model_card_template.md`

#### Refer to the modelcard.md file.
