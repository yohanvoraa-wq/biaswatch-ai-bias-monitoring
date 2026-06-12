import pandas as pd

# Load raw dataset
df = pd.read_csv("loan_approval_dataset.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Clean values
df["govt_employed"] = df["govt_employed"].astype(str).str.strip().str.lower()
df["loan_status"] = df["loan_status"].astype(str).str.strip()

# Save cleaned dataset
df.to_csv("clean_dataset.csv", index=False)

print("✅ Data cleaned and saved as clean_dataset.csv")
print(df.head())
