"""5 SQL queries mapped to realistic member questions."""

import sqlite3

import pandas as pd

conn = sqlite3.connect("coverage.db")


def run(title: str, question: str, sql: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"Q: {question}")
    print(f"--- {title} ---")
    print(sql.strip())
    print("--- result ---")
    print(pd.read_sql(sql, conn))


# 1. Deductible on Gold PPO
run(
    "Deductible lookup",
    "What's the deductible on the Gold PPO plan?",
    """
    SELECT plan_name, annual_deductible
    FROM plans
    WHERE plan_name = 'Gold PPO';
    """,
)

# 2. Pending claims for member M1001
run(
    "Pending claims by member",
    "How many claims are pending for member M1001?",
    """
    SELECT member_id, COUNT(*) AS pending_claims
    FROM claims
    WHERE member_id = 'M1001'
      AND status = 'Pending'
    GROUP BY member_id;
    """,
)

# 3. Plans under $400 monthly premium
run(
    "Premium filter",
    "Which plans have a monthly premium under $400?",
    """
    SELECT plan_id, plan_name, monthly_premium, coverage_type, network_tier
    FROM plans
    WHERE monthly_premium < 400
    ORDER BY monthly_premium;
    """,
)

# 4. JOIN claims and plans
run(
    "JOIN claims + plans",
    "Show each claim with its plan name and premium (claims JOIN plans).",
    """
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
    """,
)

# 5. Top-N most claimed procedures
run(
    "Top-N procedures",
    "What are the most claimed procedures?",
    """
    SELECT
        procedure,
        COUNT(*) AS claim_count,
        SUM(claim_amount) AS total_amount
    FROM claims
    GROUP BY procedure
    ORDER BY claim_count DESC, total_amount DESC
    LIMIT 3;
    """,
)

conn.close()
print(f"\n{'=' * 60}")
print("All 5 queries ran successfully.")
