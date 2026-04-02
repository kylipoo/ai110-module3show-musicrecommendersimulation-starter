# Collaborative Filtering:

- If two users have similar taste histories, what one enjoys can be assumed to be a good prediction for another.
- How it works:
  - Build a user-item matrix (rows = users, columns = songs, values = plays/ratings)
  - Find users with similar behavior patterns (cosine similarity, matrix factorization)
  - Recommend items those similar users liked that the target user hasn't seen
