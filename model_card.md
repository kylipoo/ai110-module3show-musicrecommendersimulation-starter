# 🎧 Model Card: Music Recommender Simulation

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

- This model suggests the top k songs (I can change how much is returned) from a small catalog based on a user's preferred genre, mood, energy and after consulting inline chat, now also checks **target_tempo**. It is for classroom exploration only, not meant to be reflective of real-world case-studies.

## 3. How It Works (Short Explanation)

For each song in the catalog, the recommender gives it a score between 0 and 1 by comparing five things about the song to what the user told us they like. The higher the score, the better the match.

**What it looks at in each song:**

- Genre (e.g. pop, rock, lofi)
- Mood (e.g. happy, intense, chill)
- Energy level — a number from 0 to 1 representing how high-energy or low-key the song feels
- Tempo — how fast the song is, measured in beats per minute
- Acousticness — how acoustic vs. electronic the song sounds

**What it knows about the user:**

- Their favorite genre and favorite mood
- Their preferred energy level (a target they want songs to match)
- Their preferred tempo
- Whether they like acoustic-sounding music or not

**How it turns those into a number:**

Each of the five features gets its own mini-score from 0 to 1. Genre and mood are all-or-nothing — a song either matches or it doesn't. Energy, tempo, and acousticness are gradual — a song that's close to your target scores nearly as well as a perfect match, and one that's far away scores lower.

Those five mini-scores are then combined into one final score using a weighted average. Energy is weighted the most heavily (40%), meaning a song that matches your energy preference will rise to the top even if the genre or mood isn't a perfect fit. Mood is second (25%), followed by genre (20%), tempo (10%), and acousticness (5%). The top-scoring songs are returned as your recommendations.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

- There are 27 songs in songs.csv.
- I added 17 more songs.
- The genres/moods MOST represented are pop, lo-fi, rock. Some suggestions AI gave along the way included jazz.
- The taste this data mostly reflects are contemporary audiences.

## 5. Strengths

You can think about:

- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

The top results worked best for the user profiles "High-energy pop" and "Deep intense rock", delivering results that came the closest to being a 1-1 match with what each profile wanted. So from what can be found here, having clear and consistent preferences that point in the same direction delivers the best results, which is indeed what's expected from a recommender.

It also handles energy-first listeners well. After reweighting energy to 40%, a user who cares most about how a song _feels_ (high-drive, fast-paced) will surface strong matches even across genre lines — Storm Runner or Gym Hero appearing near the top for an energetic profile makes sense even if the genre isn't an exact fit.

The scoring is fully transparent. Every score can be broken down into its five components, and the explanation text tells the user exactly why a song was recommended based on what attributes matched. There are no hidden factors or black-box behavior — a teacher or student can trace any result back to the math.

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:

- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

- Genre and mood matches are an all-or-nothing match (either 1.0 or 0.0). So a song that's "jazz" when you want "blues" would score identical to a song in a totally unrelated genre. This ignores real inspirations that genres could have taken from each other.
- Although when I doubled the weight given to energy for the experiment it had the benefit of being able to ignore genre lines and recommend a wider range of songs.
  - It will require very precise preferences. For example, conflicting profiles with intense mood/high energy and being in the lo-fi genre will choose results where the mood always scores 0. The system has no fallback, it just returns songs with the closest energy.
- Certain genres, moods or energy are sparse in the data-set, so users with preferences like reggae or classic might get worse recommendations.

## 7. Evaluation

How did you check your system

Examples:

- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

- I added multiple user profiles with differing genre preferences and went through each one seeing if the calculated results matched my expectations.
- **High-Energy Pop vs Chill Lofi:** The Pop profile targets energy 0.90 with non-acoustic pop songs in a happy mood,
  - **High-Energy Pop**: ![alt text](<Screenshot 2026-04-10 at 12.05.40 PM.jpg>)
  - Example for high-energy pop calculations:
    - ![alt text](<Screenshot 2026-04-03 at 11.16.33 AM.jpg>)

- **Deep Intense Rock:** Deep Intense Rock wants a target energy of 0.92 and doesn't like acoustic. It sounds similar to High energy pop, but what really makes the difference in what songs were selected was the genre attribute.
  - **Deep Intense Rock**: ![alt text](<Screenshot 2026-04-10 at 12.05.50 PM.jpg>)
  - Example for deep intense rock calculations:
    - ![alt text](<Screenshot 2026-04-10 at 10.06.46 AM.jpg>)

- **Chill Lofi** Lo-fi was a genre that I didn't give as much focus on adding songs, but it the point here was to show that even if there aren't enough songs in the database that the system will work to look at other attributes such as mood, energy and tempo.
  - **Chill Lofi**:![alt text](<Screenshot 2026-04-10 at 12.05.46 PM.jpg>)
  - Example for chill lofi calculations:
    - ![alt text](<Screenshot 2026-04-10 at 10.16.53 AM.jpg>)

- **Lofi Rager (with comparison to deep intense rock):** Lo-fi rager targets high energy (~0.90+) and prefers non-acoustic. On paper it sounds like rock songs would probably get a lot of attention. Rock gets excellent results because the catalog has many intense rock songs that match all its attributes. The Lofi Rager, despite having the same energy target, gets poor results because fundamentally it's impossible to have a song that's high energy but also Lo-fi, as one of them is known for being intense and loud while Lo-fi is more something you can listen to while doing something else and not have it disrupt your activity. Additionally, I would also like to bring to mind that when I shifted the weights to be more forcused on energy
  - **Deep Intense Rock**: ![alt text](<Screenshot 2026-04-10 at 12.05.50 PM-1.jpg>)
  - **Lofi Rager**: ![alt text](<Screenshot 2026-04-10 at 12.06.01 PM.jpg>)
  - Example for lofi rager calculations:
    - ![alt text](<Screenshot 2026-04-10 at 10.24.46 AM.jpg>)
  - In addition, it's worth noting that when I had changed the weight to be more focused on energy, my search results changed. Previously, the algorithm would try to at least search for songs matching the lofi genre but now since genre is less important, it will look for more rock songs like Bohemian Rhapsody.
    - **Lofi Rager after changes**:
      - ![alt text](<Screenshot 2026-04-10 at 12.10.25 PM.jpg>)

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

- I would add more diverse genres and balance the current selection out.
- I would add more attributes like what kind of instruments are being used, the volume, if the song contains any mature themes.
- I actually plan on making this project the subject of the final project where I need to implement RAG.
  - A meaningful extension would be to augment the numeric scoring with a RAG layer that retrieves text-based context about each song — artist interviews, critical reviews, lyric analysis, or cultural background — and uses a language model to reason over that context alongside the numeric match. This would let the system distinguish songs that are numerically identical but emotionally different, and surface recommendations based on meaning rather than just measurement. For example, two songs at 140 BPM with energy 0.92 might score identically today, but one was written as a celebration another as a breakdown. This is based on personal experience, I saw a video once pointing out two songs had the same key (tonal center/musical scale) yet one of them was from the Minecraft movie and was light hearted and talking about lava chicken, the other was from death note and it was meant to display the crashout and mental decay of the protagonist.

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

I was surprised that even features most don't think about when they listen to a song, like tempo can be important, as that was one of the recommendations Claude gave to make song scoring more accurate.

Building this system showed me that every weight shift has cascading consequences on the entire ranking. When I doubled the energy weight from 0.20 to 0.40, songs that were buried suddenly surfaced — not because they became better matches, but because I changed what the system was willing to prioritize. Those decisions look like math, but they're not neutral. And even when the weights feel right, scoring alone doesn't tell the full picture: genre is treated as a binary label, so if you asked for "heavy metal," every rock song in the catalog would score a 0 on genre — even though most listeners would instinctively know the two are closely related. The system has no concept of proximity between categories, only exact matches.

That drift points to where human judgment stays irreplaceable. A score can tell you two songs share the same energy and BPM, but it can't tell you one feels like a rainy afternoon, or that the other is the song from a video game that defined someone's childhood. Numbers describe a song's surface; what makes a song matter lives somewhere no feature vector can reach.
