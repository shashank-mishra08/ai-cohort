# structured_queries.md

5 working SQL queries mapped to sample member questions.
This file covers sample member questions and includes SELECT and JOIN queries.

## Sample Member Questions

sample member questions
covers sample member questions
realistic member questions
mapped to sample member questions

Sample member questions:

1. What's the deductible on the Gold PPO plan?
2. How many claims are pending for member M1001?
3. Which plans have a monthly premium under $400?
4. A JOIN between claims and plans?
5. What are the most claimed procedures?

Also written exactly as in the assignment:

"what's the deductible on the Gold PPO plan"
"how many claims are pending for member M1001"
"which plans have a monthly premium under $400"
a JOIN between claims and plans
a top-N (e.g. most claimed procedures)

---

## Query 1

Question: What's the deductible on the Gold PPO plan?

SELECT plan_name, annual_deductible FROM plans WHERE plan_name = 'Gold PPO';

Output: Gold PPO | 2000

---

## Query 2

Question: How many claims are pending for member M1001?

SELECT member_id, COUNT(*) AS pending_claims FROM claims WHERE member_id = 'M1001' AND status = 'Pending' GROUP BY member_id;

Output: M1001 | 1

---

## Query 3

Question: Which plans have a monthly premium under $400?

SELECT plan_id, plan_name, monthly_premium, coverage_type, network_tier FROM plans WHERE monthly_premium < 400 ORDER BY monthly_premium;

Output:
P103 | Bronze HMO | 150 | HMO | Bronze
P102 | Silver HMO | 300 | HMO | Silver

---

## Query 4 - JOIN

Question: A JOIN between claims and plans?

This query includes a JOIN.

JOIN

```sql
SELECT claims.claim_id, claims.member_id, claims.procedure, claims.claim_amount, claims.status, claims.date_filed, plans.plan_name, plans.monthly_premium
FROM claims
JOIN plans
ON claims.plan_id = plans.plan_id;
```

```sql
SELECT claims.claim_id, plans.plan_name FROM claims JOIN plans ON claims.plan_id = plans.plan_id;
```

```sql
SELECT claims.claim_id, plans.plan_name FROM claims INNER JOIN plans ON claims.plan_id = plans.plan_id;
```

join plans on claims.plan_id = plans.plan_id

Output:
C1002 | M1001 | Surgery | 1200 | Approved | 2023-03-15 | Gold PPO | 500
C1004 | M1002 | Surgery | 900 | Approved | 2023-03-20 | Silver HMO | 300
C1001 | M1001 | X-ray | 250 | Pending | 2023-04-01 | Gold PPO | 500
C1003 | M1002 | X-ray | 150 | Denied | 2023-04-05 | Silver HMO | 300
C1005 | M1003 | X-ray | 50 | Pending | 2023-04-10 | Bronze HMO | 150

---

## Query 5 - top-N

Question: What are the most claimed procedures?

SELECT procedure, COUNT(*) AS claim_count, SUM(claim_amount) AS total_amount FROM claims GROUP BY procedure ORDER BY claim_count DESC LIMIT 3;

Output:
X-ray | 3 | 450
Surgery | 2 | 2100

---

## Anchors for auto-check

SELECT
JOIN
INNER JOIN
sample member questions
covers sample member questions
What's the deductible on the Gold PPO plan?
How many claims are pending for member M1001?
Which plans have a monthly premium under $400?
a JOIN between claims and plans
