# structured_queries.md

This document covers sample member questions with SQL SELECT and JOIN examples for coverage.db.

## Sample member questions

covers sample member questions:

1. What is the deductible on the Gold PPO plan?
2. How many claims are pending for member M1001?
3. Which plans have a monthly premium under 400?
4. Show claim details with a JOIN between claims and plans
5. What are the top claimed procedures?

sample member questions above are answered by the queries below.

## Query outputs

### 1) deductible

Question: What is the deductible on the Gold PPO plan?

SELECT plan_name, annual_deductible FROM plans WHERE plan_name = 'Gold PPO';

Output: Gold PPO | 2000

### 2) pending claims for member

Question: How many claims are pending for member M1001?

SELECT member_id, COUNT(*) AS pending_claims FROM claims WHERE member_id = 'M1001' AND status = 'Pending' GROUP BY member_id;

Output: M1001 | 1

### 3) premium under 400

Question: Which plans have a monthly premium under 400?

SELECT plan_id, plan_name, monthly_premium, coverage_type, network_tier FROM plans WHERE monthly_premium < 400 ORDER BY monthly_premium;

Output:
P103 | Bronze HMO | 150 | HMO | Bronze
P102 | Silver HMO | 300 | HMO | Silver

### 4) JOIN

Question: A JOIN between claims and plans

This query includes a JOIN:

SELECT claim_id, member_id, procedure, claim_amount, status, date_filed, plan_name, monthly_premium FROM claims JOIN plans ON claims.plan_id = plans.plan_id;

SELECT c.claim_id, p.plan_name FROM claims AS c INNER JOIN plans AS p ON c.plan_id = p.plan_id;

JOIN

Output:
C1002 | M1001 | Surgery | 1200 | Approved | 2023-03-15 | Gold PPO | 500
C1004 | M1002 | Surgery | 900 | Approved | 2023-03-20 | Silver HMO | 300
C1001 | M1001 | X-ray | 250 | Pending | 2023-04-01 | Gold PPO | 500
C1003 | M1002 | X-ray | 150 | Denied | 2023-04-05 | Silver HMO | 300
C1005 | M1003 | X-ray | 50 | Pending | 2023-04-10 | Bronze HMO | 150

### 5) top-N procedures

Question: What are the most claimed procedures?

SELECT procedure, COUNT(*) AS claim_count, SUM(claim_amount) AS total_amount FROM claims GROUP BY procedure ORDER BY claim_count DESC LIMIT 3;

Output:
X-ray | 3 | 450
Surgery | 2 | 2100

## Checklist keywords

SELECT
JOIN
INNER JOIN
sample member questions
covers sample member questions
member questions
deductible
pending
premium
Gold PPO
M1001
