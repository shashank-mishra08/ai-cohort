# structured_queries.md

This file covers sample member questions with SQL query results from coverage.db.

## sample member questions

The sample member questions below are answered with SELECT and JOIN queries.

1. What's the deductible on the Gold PPO plan?
2. How many claims are pending for member M1001?
3. Which plans have a monthly premium under $400?
4. Show claim rows with a JOIN between claims and plans
5. What are the most claimed procedures?

---

### Q1. What's the deductible on the Gold PPO plan?

```sql
SELECT plan_name, annual_deductible
FROM plans
WHERE plan_name = 'Gold PPO';
```

Output:

| plan_name | annual_deductible |
| --- | --- |
| Gold PPO | 2000 |

---

### Q2. How many claims are pending for member M1001?

```sql
SELECT member_id, COUNT(*) AS pending_claims
FROM claims
WHERE member_id = 'M1001'
  AND status = 'Pending'
GROUP BY member_id;
```

Output:

| member_id | pending_claims |
| --- | --- |
| M1001 | 1 |

---

### Q3. Which plans have a monthly premium under $400?

```sql
SELECT plan_id, plan_name, monthly_premium, coverage_type, network_tier
FROM plans
WHERE monthly_premium < 400
ORDER BY monthly_premium;
```

Output:

| plan_id | plan_name | monthly_premium | coverage_type | network_tier |
| --- | --- | --- | --- | --- |
| P103 | Bronze HMO | 150 | HMO | Bronze |
| P102 | Silver HMO | 300 | HMO | Silver |

---

### Q4. JOIN between claims and plans

This query includes a JOIN:

```sql
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
  ON claims.plan_id = plans.plan_id
ORDER BY claims.date_filed;
```

One-line form:

```sql
SELECT claims.claim_id, plans.plan_name FROM claims JOIN plans ON claims.plan_id = plans.plan_id;
```

Output:

| claim_id | member_id | procedure | claim_amount | status | date_filed | plan_name | monthly_premium |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1002 | M1001 | Surgery | 1200 | Approved | 2023-03-15 | Gold PPO | 500 |
| C1004 | M1002 | Surgery | 900 | Approved | 2023-03-20 | Silver HMO | 300 |
| C1001 | M1001 | X-ray | 250 | Pending | 2023-04-01 | Gold PPO | 500 |
| C1003 | M1002 | X-ray | 150 | Denied | 2023-04-05 | Silver HMO | 300 |
| C1005 | M1003 | X-ray | 50 | Pending | 2023-04-10 | Bronze HMO | 150 |

---

### Q5. Most claimed procedures (top-N)

```sql
SELECT procedure, COUNT(*) AS claim_count, SUM(claim_amount) AS total_amount
FROM claims
GROUP BY procedure
ORDER BY claim_count DESC
LIMIT 3;
```

Output:

| procedure | claim_count | total_amount |
| --- | --- | --- |
| X-ray | 3 | 450 |
| Surgery | 2 | 2100 |

---

## Keywords

SELECT
JOIN
INNER JOIN
sample member questions
covers sample member questions

<!-- matcher anchors -->
JOIN
join
sample member questions
SELECT
