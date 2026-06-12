import pandas as pd

# Load cleaned data
df = pd.read_csv("clean_dataset.csv")

# Separate govt and non-govt applicants
govt_df = df[df["govt_employed"] == "yes"]
nongovt_df = df[df["govt_employed"] == "no"]

# Decide BEFORE size (60% of data)
before_size = int(0.6 * len(df))

# Govt-heavy BEFORE (70% govt, 30% non-govt)
govt_count = int(0.7 * before_size)
nongovt_count = before_size - govt_count

# Safe sampling
before_govt = govt_df.sample(n=min(govt_count, len(govt_df)), random_state=42)
before_nongovt = nongovt_df.sample(n=min(nongovt_count, len(nongovt_df)), random_state=42)

before_df = pd.concat([before_govt, before_nongovt])
after_df = df.drop(before_df.index)

# Save datasets
before_df.to_csv("before_shift.csv", index=False)
after_df.to_csv("after_shift.csv", index=False)

# Sanity checks
print("✅ Segregation complete")

print("\nBEFORE shift distribution:")
print(before_df["govt_employed"].value_counts(normalize=True))

print("\nAFTER shift distribution:")
print(after_df["govt_employed"].value_counts(normalize=True))
