# Structured SQL Queries — coverage.db

Reference for the 5 member-facing questions and their SQL against `coverage.db` (`plans`, `claims`).

Generated from `queries.py` against cleaned data loaded via `main.py`.

---

## 1. Deductible lookup

**Question:** What's the deductible on the Gold PPO plan?

**SQL:**

```sql
SELECT plan_name, annual_deductible
FROM plans
WHERE plan_name = 'Gold PPO';
```

**Output:**

| plan_name | annual_deductible |
|-----------|-------------------|
| Gold PPO  | 2000              |

**Notes:** Simple filtered lookup on `plans`. Annual deductible for Gold PPO is **$2,000**.

---

## 2. Pending claims by member

**Question:** How many claims are pending for member M1001?

**SQL:**

```sql
SELECT member_id, COUNT(*) AS pending_claims
FROM claims
WHERE member_id = 'M1001'
  AND status = 'Pending'
GROUP BY member_id;
```

**Output:**

| member_id | pending_claims |
|-----------|----------------|
| M1001     | 1              |

**Notes:** Aggregate with two filters (`member_id`, `status`). Member M1001 has **1** pending claim.

---

## 3. Premium filter

**Question:** Which plans have a monthly premium under $400?

**SQL:**

```sql
SELECT plan_id, plan_name, monthly_premium, coverage_type, network_tier
FROM plans
WHERE monthly_premium < 400
ORDER BY monthly_premium;
```

**Output:**

| plan_id | plan_name  | monthly_premium | coverage_type | network_tier |
|---------|------------|-----------------|---------------|--------------|
| P103    | Bronze HMO | 150             | HMO           | Bronze       |
| P102    | Silver HMO | 300             | HMO           | Silver       |

**Notes:** Range filter on premium. Gold PPO ($500) is excluded. Two plans under $400, ordered cheapest first.

---

## 4. JOIN claims + plans

**Question:** Show each claim with its plan name and premium (claims JOIN plans).

**SQL:**

```sql
SELECT
    c.claim_id,
    c.member_id,
    c.procedure,
    c.claim_amount,
    c.status,
    c.date_filed,
    p.plan_name,
    p.monthly_premium,
    p.coverage_type
FROM claims AS c
INNER JOIN plans AS p
    ON c.plan_id = p.plan_id
ORDER BY c.date_filed;
```

**Output:**

| claim_id | member_id | procedure | claim_amount | status   | date_filed          | plan_name  | monthly_premium | coverage_type |
|----------|-----------|-----------|--------------|----------|---------------------|------------|-----------------|---------------|
| C1002    | M1001     | Surgery   | 1200         | Approved | 2023-03-15 00:00:00 | Gold PPO   | 500             | PPO           |
| C1004    | M1002     | Surgery   | 900          | Approved | 2023-03-20 00:00:00 | Silver HMO | 300             | HMO           |
| C1001    | M1001     | X-ray     | 250          | Pending  | 2023-04-01 00:00:00 | Gold PPO   | 500             | PPO           |
| C1003    | M1002     | X-ray     | 150          | Denied   | 2023-04-05 00:00:00 | Silver HMO | 300             | HMO           |
| C1005    | M1003     | X-ray     | 50           | Pending  | 2023-04-10 00:00:00 | Bronze HMO | 150             | HMO           |

**Notes:** `INNER JOIN` on `plan_id` enriches each claim with plan attributes. All 5 claims matched a plan.

---

## 5. Top-N most claimed procedures

**Question:** What are the most claimed procedures?

**SQL:**

```sql
SELECT
    procedure,
    COUNT(*) AS claim_count,
    SUM(claim_amount) AS total_amount
FROM claims
GROUP BY procedure
ORDER BY claim_count DESC, total_amount DESC
LIMIT 3;
```

**Output:**

| procedure | claim_count | total_amount |
|-----------|-------------|--------------|
| X-ray     | 3           | 450          |
| Surgery   | 2           | 2100         |

**Notes:** Classic top-N: `GROUP BY` + `ORDER BY COUNT DESC` + `LIMIT`. **X-ray** is most frequent (3 claims); **Surgery** has higher total amount ($2,100).

---

## How to re-run

```bash
source .venv/bin/activate
python main.py      # rebuild coverage.db from CSVs
python queries.py    # print live query results
```

Database file: `coverage.db`  
Tables: `plans` (3 rows), `claims` (5 rows)
