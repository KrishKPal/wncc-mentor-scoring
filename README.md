# Mentor Evaluation Model

A structured, data-driven framework to evaluate mentor effectiveness in a college mentoring program under incomplete and noisy data conditions.

The model combines multiple signals—student progress, responsiveness, engagement, and feedback—into a single normalized score while accounting for bias, sparsity, and scale differences.

---

## Problem Context

Evaluating mentor performance in a college setting is challenging because:

- Multiple mentors may supervise the same student  
- Interaction data is noisy and incomplete  
- Feedback is subjective and sparse  
- Raw activity metrics are not directly comparable  

This project builds a robust scoring model to address these issues.

---

## Model Overview

Final mentor score:

M(m) = 0.40P + 0.30R + 0.15E + 0.15F

Where:

- **P** → Student progress (weighted milestones)  
- **R** → Responsiveness (nonlinear penalty using Hill function)  
- **E** → Engagement (normalized interaction intensity)  
- **F** → Feedback (Bayesian-smoothed ratings)  

---

## Key Design Choices

### 1. Weighted Progress Modeling
- Later milestones contribute more using triangular weighting  
- Prevents early-stage completion from dominating score  

---

### 2. Nonlinear Responsiveness (Hill Function)
- Flat reward for fast replies  
- Sharp penalty after delay threshold  
- Better reflects real-world productivity impact than exponential decay  

---

### 3. Engagement Normalization
- Computed per mentee to avoid bias from mentor workload  
- Min-max scaled across mentors  

---

### 4. Bayesian Feedback Smoothing
- Prevents small sample bias  
- Incorporates global prior  
- Down-weights outlier ratings instead of removing them  

---

## Data Challenges & Handling

- Duplicate names → resolved using ID-based joins  
- Shared students → full credit assigned due to lack of attribution data  
- Missing interactions → treated as zero contribution  
- Nonlinear metrics → computed before aggregation  

---

## Statistical Observations

- Engagement has weak correlation with actual progress  
- Feedback aligns more with perceived support than outcomes  

This motivated prioritizing outcome-based and responsiveness signals in final weighting.

---

## Limitations

- No timestamps → cannot model time evolution  
- Weights are heuristic (not learned from data)  
- Feedback may reflect perception rather than true effectiveness  
- Cannot split contribution among multiple mentors  

---

## Possible Improvements

- Learn weights using regression or ranking models  
- Introduce time-based decay with real timestamps  
- Attribute contribution among multiple mentors  
- Validate scores against long-term student outcomes  

---

## Tech Stack

- Python  
- Pandas  
- NumPy  

---

## Output

- Mentor ranking leaderboard  
- Component-wise score breakdown  
- Normalized and comparable evaluation across mentors  

---

## Why not a simple average?

A naive scoring approach (e.g., averaging meetings, messages, and ratings) fails because:

- Metrics exist on different scales  
- Some signals are noisy or biased  
- Nonlinear effects (like response delay) matter  
- Mentor workload varies significantly  

This model addresses these issues through normalization, nonlinear scoring, and smoothing.

---
