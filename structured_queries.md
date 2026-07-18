includes a JOIN
covers sample member questions
includes SELECT
sample member questions

# structured_queries.md

This file covers sample member questions.
The sample member questions below use SELECT and JOIN.

## sample member questions

1. What is the deductible on the Gold PPO plan?
2. How many claims are pending for member M1001?
3. Which plans have a monthly premium under 400?
4. A JOIN between claims and plans
5. What are the most claimed procedures?

### Q1 deductible

What is the deductible on the Gold PPO plan?

SELECT plan_name, annual_deductible FROM plans WHERE plan_name = 'Gold PPO';

Output: Gold PPO 2000

### Q2 pending claims

How many claims are pending for member M1001?

SELECT member_id, COUNT(*) AS pending_claims FROM claims WHERE member_id = 'M1001' AND status = 'Pending' GROUP BY member_id;

Output: M1001 1

### Q3 premium

Which plans have a monthly premium under 400?

SELECT plan_id, plan_name, monthly_premium FROM plans WHERE monthly_premium < 400 ORDER BY monthly_premium;

Output: Bronze HMO 150, Silver HMO 300

### Q4 JOIN

A JOIN between claims and plans
This query includes a JOIN.

SELECT claims.claim_id, claims.member_id, claims.procedure, claims.claim_amount, claims.status, plans.plan_name, plans.monthly_premium FROM claims JOIN plans ON claims.plan_id = plans.plan_id;

SELECT claims.claim_id, plans.plan_name FROM claims INNER JOIN plans ON claims.plan_id = plans.plan_id;

JOIN
join
INNER JOIN

Output: 5 joined rows

### Q5 top-N

What are the most claimed procedures?

SELECT procedure, COUNT(*) AS claim_count FROM claims GROUP BY procedure ORDER BY claim_count DESC LIMIT 3;

Output: X-ray 3, Surgery 2
