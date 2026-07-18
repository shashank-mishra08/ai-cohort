import sqlite3

import pandas as pd

# 1. Load both CSVs
claims = pd.read_csv("data/claims.csv")
plans = pd.read_csv("data/plan.csv")

# 2. Inspect
print("=== CLAIMS ===")
claims.info()
print(claims.head())
print("\nNulls (claims):\n", claims.isnull().sum())

print("\n=== PLANS ===")
plans.info()
print(plans.head())
print("\nNulls (plans):\n", plans.isnull().sum())

# 3. Clean
claims = claims.drop_duplicates()
plans = plans.drop_duplicates()

claims["status"] = claims["status"].fillna("Unknown")
claims["claim_amount"] = claims["claim_amount"].fillna(0)
claims = claims.dropna(subset=["claim_id", "member_id", "plan_id", "date_filed"])

claims["date_filed"] = pd.to_datetime(claims["date_filed"], errors="coerce")
claims = claims.dropna(subset=["date_filed"])

plans = plans.dropna(subset=["plan_id"])

# 4. Verify cleaning
print("\n=== AFTER CLEAN ===")
print(claims.dtypes)
print(claims["date_filed"].head())
print("claims rows:", len(claims), "| plans rows:", len(plans))

# 5. Merge on plan_id
df = claims.merge(plans, on="plan_id", how="left")
print("\n=== MERGED ===")
print(df.head())
print("merged rows:", len(df))
print(df.info())

# 6. Create coverage.db and load cleaned tables
conn = sqlite3.connect("coverage.db")
plans.to_sql("plans", conn, if_exists="replace", index=False)
claims.to_sql("claims", conn, if_exists="replace", index=False)

# Verify tables
print("\n=== SQLITE ===")
print("tables:", conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
print("plans count:", conn.execute("SELECT COUNT(*) FROM plans").fetchone()[0])
print("claims count:", conn.execute("SELECT COUNT(*) FROM claims").fetchone()[0])
print(pd.read_sql("SELECT * FROM plans LIMIT 3", conn))
print(pd.read_sql("SELECT * FROM claims LIMIT 3", conn))
conn.close()
print("Saved: coverage.db")
