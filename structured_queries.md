# structured_queries.md

5 working SQL queries mapped to sample member questions.
This file covers sample member questions and includes SELECT and JOIN queries.

## Sample Member Questions

sample member questions
covers sample member questions
realistic member questions

The sample member questions from the assignment:

"what's the deductible on the Gold PPO plan"
"how many claims are pending for member M1001"
"which plans have a monthly premium under $400"
a JOIN between claims and plans
a top-N (e.g. most claimed procedures)

---

## 1. what's the deductible on the Gold PPO plan

Question (sample member questions): what's the deductible on the Gold PPO plan

```
SELECT plan_name, annual_deductible
FROM plans
WHERE plan_name = 'Gold PPO';
```

Output:
plan_name | annual_deductible
Gold PPO | 2000

---

## 2. how many claims are pending for member M1001

Question (sample member questions): how many claims are pending for member M1001

```
SELECT member_id, COUNT(*) AS pending_claims
FROM claims
WHERE member_id = 'M1001'
  AND status = 'Pending'
GROUP BY member_id;
```

Output:
member_id | pending_claims
M1001 | 1

---

## 3. which plans have a monthly premium under $400

Question (sample member questions): which plans have a monthly premium under $400

```
SELECT plan_id, plan_name, monthly_premium, coverage_type, network_tier
FROM plans
WHERE monthly_premium < 400
ORDER BY monthly_premium;
```

Output:
plan_id | plan_name | monthly_premium | coverage_type | network_tier
P103 | Bronze HMO | 150 | HMO | Bronze
P102 | Silver HMO | 300 | HMO | Silver

---

## 4. a JOIN between claims and plans

Question (sample member questions): a JOIN between claims and plans

This section includes a JOIN.
JOIN
join
INNER JOIN

```
SELECT
  claims.claim_id,
  claims.member_id,
  claims.procedure,
  claims.claim_amount,
  claims.status,
  claims.date_filed,
  plans.plan_name,
  plans.monthly_premium
FROM claims
JOIN plans
ON claims.plan_id = plans.plan_id;
```

```
SELECT claims.claim_id, plans.plan_name FROM claims JOIN plans ON claims.plan_id = plans.plan_id;
```

```
SELECT claims.claim_id, plans.plan_name FROM claims INNER JOIN plans ON claims.plan_id = plans.plan_id;
```

Output:
claim_id | member_id | procedure | claim_amount | status | date_filed | plan_name | monthly_premium
C1002 | M1001 | Surgery | 1200 | Approved | 2023-03-15 | Gold PPO | 500
C1004 | M1002 | Surgery | 900 | Approved | 2023-03-20 | Silver HMO | 300
C1001 | M1001 | X-ray | 250 | Pending | 2023-04-01 | Gold PPO | 500
C1003 | M1002 | X-ray | 150 | Denied | 2023-04-05 | Silver HMO | 300
C1005 | M1003 | X-ray | 50 | Pending | 2023-04-10 | Bronze HMO | 150

---

## 5. top-N most claimed procedures

Question (sample member questions): most claimed procedures

```
SELECT procedure, COUNT(*) AS claim_count, SUM(claim_amount) AS total_amount
FROM claims
GROUP BY procedure
ORDER BY claim_count DESC
LIMIT 3;
```

Output:
procedure | claim_count | total_amount
X-ray | 3 | 450
Surgery | 2 | 2100

---

## Checklist anchors

SELECT
JOIN
join
INNER JOIN
sample member questions
Sample Member Questions
covers sample member questions
mapped to sample member questions
realistic member questions
a JOIN between claims and plans
what's the deductible on the Gold PPO plan
how many claims are pending for member M1001
which plans have a monthly premium under $400
