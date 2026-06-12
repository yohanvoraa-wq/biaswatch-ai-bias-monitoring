import pandas as pd

# Load AFTER dataset (original)
df = pd.read_csv("after_shift.csv")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Normalize values
df["govt_employed"] = df["govt_employed"].astype(str).str.strip().str.lower()
df["loan_status"] = df["loan_status"].astype(str).str.strip()

print("\nLoan status distribution BEFORE injection:")
print(df["loan_status"].value_counts())

# Select non-govt approved applicants
mask = (df["govt_employed"] == "no") & (df["loan_status"] == "Approved")

eligible = mask.sum()
print(f"\nEligible non-govt approved rows: {eligible}")

if eligible == 0:
    print("❌ No rows eligible for bias injection. Check data.")
else:
    # Flip 30% of eligible approvals
    flip_count = int(0.3 * eligible)

    flip_indices = df[mask].sample(
        n=flip_count,
        random_state=42
    ).index

    df.loc[flip_indices, "loan_status"] = "Rejected"

    # Save as NEW file
    df.to_csv("after_shift_biased.csv", index=False)

    print(f"✅ Injected bias into {flip_count} rows.")
    print("📁 Saved as after_shift_biased.csv")
