import pandas as pd

# -----------------------------
# Load and normalize dataset
# -----------------------------
def load_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()
    df["govt_employed"] = df["govt_employed"].str.lower()
    df["loan_status"] = df["loan_status"].str.strip()
    return df

# -----------------------------
# Compute approval rate
# -----------------------------
def compute_metrics(df):
    metrics = {}

    for group in ["yes", "no"]:
        gdf = df[df["govt_employed"] == group]
        total = len(gdf)

        if total == 0:
            continue

        approved = (gdf["loan_status"] == "Approved").sum()
        approval_rate = approved / total

        metrics[group] = {
            "total_applicants": total,
            "approval_rate": round(approval_rate, 3)
        }

    return metrics

# -----------------------------
# Bias drift detection
# -----------------------------
def detect_bias(metrics, threshold=0.15):
    if "yes" not in metrics or "no" not in metrics:
        return False, 0.0

    diff = abs(
        metrics["yes"]["approval_rate"]
        - metrics["no"]["approval_rate"]
    )

    return diff > threshold, round(diff, 3)

# -----------------------------
# Main
# -----------------------------
def main():
    before_df = load_data("before_shift.csv")
    after_df = load_data("after_shift_biased.csv")

    before_metrics = compute_metrics(before_df)
    after_metrics = compute_metrics(after_df)

    print("\n===== BEFORE SHIFT METRICS =====")
    print(before_metrics)

    print("\n===== AFTER SHIFT METRICS =====")
    print(after_metrics)

    drift, diff = detect_bias(after_metrics)

    print("\n===== BIAS DRIFT CHECK =====")
    print("Approval rate difference:", diff)

    if drift:
        print("🚨 BIAS DRIFT DETECTED")
    else:
        print("✅ No significant bias drift detected")

if __name__ == "__main__":
    main()
