# wncc-mentor-scoring
This project computes a ranked mentor leaderboard for the WnCC Convenor Assignment 2026-27, Question 1. The system combines student progress, responsiveness, engagement, and mentee feedback into a single mentor score.

## Output

The output contains:

- `MentorID`
- `Name`
- `FinalScore`
- `Rank`

Mentors are sorted in descending order of `FinalScore`.

## Design Summary

The final mentor score is:
```text
M(m) = 0.40P + 0.30R + 0.15E + 0.15F
```

Where:
- `P` is a weighted student progress ratio 
- `R` is a Hill-function responsiveness score
- `E` is a per-mentee engagement score based on meetings,messages and code reviews.
- `F` is a Bayesian-smoothed feedback score with outlier down-weighting

### *More details and justification are provided in `ideation.md` file .*

## Important Note :

- All joins are done using `MentorID` and `StudentID`, not names, because names are duplicated in the dataset.
- Any student may have multiple mentors. In that case, each mentor receives full credit for that student’s progress because the dataset does not attribute individually.
- Mentors with no recorded interactions or feedback are assigned zero for unavailable components.
