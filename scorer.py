#grace time for response - grace
# engagweights - e_w
# finalWeights - w
# progress per mentor is p_pm
#responsiveness per mentor is r_pm
#engagement per mentor is e_pm
# feedback per mentor is f_pm



from pathlib import Path
import numpy as np
import pandas as pd

DATA_DIR = Path("data")
OUTPUT_FILE = Path("mentor_scores.csv")
grace = 4.0
tau = 8.0
k_hill = np.log(19) / np.log(2.5)


e_w = { "Meetings": 0.5, "CodeReviews": 0.3,"Messages": 0.2}

w = { "P": 0.40, "R": 0.30, "E": 0.15, "F": 0.15}

prior_weight = 3

def hill_r(t: float) -> float:
    if t <= grace:
        return 1.0
    return 1.0 / (1.0 + ((t - grace) / tau) ** k_hill)

def minmax(s: pd.Series) -> pd.Series:
    mn = s.min()
    mx = s.max()
    if pd.isna(mx) or pd.isna(mn) or mx == mn:
        return pd.Series(0.0, index=s.index)
    return (s - mn) / (mx - mn)

def fb_score(g: pd.DataFrame, mu: float) -> float:
    ratings = g["Rating"].astype(float).to_numpy()
    n = len(ratings)

    if n >= 3:
        r_bar = ratings.mean()
        sigma = ratings.std()
        if sigma > 0:
            z = np.abs((ratings - r_bar) / sigma)
            wt = np.where(z > 2, 0.5, 1.0)
        else:
            wt = np.ones(n)
        r_bar_w = np.average(ratings, weights=wt)
    else:
        r_bar_w = ratings.mean()

    f_smooth = (n * r_bar_w + prior_weight * mu) / (n + prior_weight)
    return (f_smooth - 1.0) / 4.0

def main() -> None:
    mentors = pd.read_csv(DATA_DIR / "mentors.csv")
    students = pd.read_csv(DATA_DIR / "students.csv")
    inter = pd.read_csv(DATA_DIR / "interactions.csv")
    fb = pd.read_csv(DATA_DIR / "feedbacks.csv")

    students["weighted_completed"] = (
        students["MilestonesCompleted"] * (students["MilestonesCompleted"] + 1) / 2
    )
    students["weighted_total"] = (
        students["TotalMilestones"] * (students["TotalMilestones"] + 1) / 2
    )

    p_pm = (
        inter[["MentorID", "StudentID"]]
        .merge(
            students[["StudentID", "weighted_completed", "weighted_total"]],
            on="StudentID",
            how="left",
        )
        .groupby("MentorID", as_index=False)[["weighted_completed", "weighted_total"]]
        .sum()
    )
    p_pm["P"] = p_pm["weighted_completed"] / p_pm["weighted_total"]

    inter["R_pair"] = inter["AvgResponseTime"].apply(hill_r)
    r_pm = (
        inter.groupby("MentorID", as_index=False)["R_pair"]
        .mean()
        .rename(columns={"R_pair": "R"})
    )

    inter["E_raw"] = ( e_w["Meetings"] * inter["Meetings"] + e_w["CodeReviews"] * inter["CodeReviews"]  + e_w["Messages"] * inter["Messages"])

    studentCount = inter.groupby("MentorID")["StudentID"].nunique().rename("n_students")
    e_pm = (
        inter.groupby("MentorID", as_index=False)["E_raw"]
        .sum()
        .rename(columns={"E_raw": "E_sum"})
        .merge(studentCount, on="MentorID", how="left")
    )
    e_pm["E_per_mentee"] = e_pm["E_sum"] / e_pm["n_students"]
    e_pm["E"] = minmax(e_pm["E_per_mentee"])

    mu = fb["Rating"].mean()
    f_pm = (
        fb.groupby("MentorID")
        .apply(lambda g: fb_score(g, mu), include_groups=False)
        .reset_index(name="F")
    )

    scores = mentors[["MentorID", "Name"]].copy()
    scores = scores.merge(p_pm[["MentorID", "P"]], on="MentorID", how="left")
    scores = scores.merge(r_pm, on="MentorID", how="left")
    scores = scores.merge(e_pm[["MentorID", "E"]], on="MentorID", how="left")
    scores = scores.merge(f_pm, on="MentorID", how="left")

    scores[["P", "R", "E", "F"]] = scores[["P", "R", "E", "F"]].fillna(0.0)
    scores["FinalScore"] = (
        w["P"]*scores["P"] +w["R"]*scores["R"] + w["E"]*scores["E"] + w["F"]*scores["F"] )
    scores = scores.sort_values(
        by=["FinalScore", "P", "R", "E", "F", "MentorID"],ascending=[False, False, False, False, False, True]).reset_index(drop=True)

    scores["Rank"] = scores.index + 1

    output = scores[["MentorID", "Name", "FinalScore", "Rank"]].copy()
    output["FinalScore"] = output["FinalScore"].round(4)
    output.to_csv(OUTPUT_FILE, index=False)

    print(output.to_string(index=False))
    print(f"\nTotal mentors scored: {len(output)}")


if __name__ == "__main__":
    main()
