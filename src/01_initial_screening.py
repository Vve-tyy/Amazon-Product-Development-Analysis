from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT_DIR / "data" / "raw" / "candidate_products_2.csv"
OUTPUT_FILE = ROOT_DIR / "data" / "processed" / "initial_screening_result.csv"

df = pd.read_csv(INPUT_FILE)

# 1. 数据质量检查
print("=== 数据质量检查 ===")
print(f"数据行数：{len(df)}")
print(f"重复 Product_ID：{df['Product_ID'].duplicated().sum()}")
print(f"缺失值总数：{df.isnull().sum().sum()}")

required_columns = [
    "Target_Price_USD",
    "Estimated_Monthly_Sales",
    "Search_Trend_Growth_Pct",
    "Estimated_Competitor_Count",
    "Estimated_Gross_Margin_Pct",
]

if (df[required_columns] < 0).any().any():
    raise ValueError("发现负数数据，请检查原始数据集。")

# 2. 初筛门槛
df["Pass_Sales"] = df["Estimated_Monthly_Sales"] >= 2000
df["Pass_Trend"] = df["Search_Trend_Growth_Pct"] >= 10
df["Pass_Competition"] = df["Estimated_Competitor_Count"] <= 80
df["Pass_Margin"] = df["Estimated_Gross_Margin_Pct"] >= 30

# 3. 初筛评分：满分 100
df["Demand_Score"] = (
    df["Estimated_Monthly_Sales"].clip(upper=4000) / 4000 * 30
).round(1)

df["Trend_Score"] = (
    df["Search_Trend_Growth_Pct"].clip(upper=20) / 20 * 20
).round(1)

df["Competition_Score"] = (
    ((100 - df["Estimated_Competitor_Count"]).clip(lower=0) / 100) * 20
).round(1)

df["Margin_Score"] = (
    df["Estimated_Gross_Margin_Pct"].clip(upper=45) / 45 * 20
).round(1)

# 评分较低代表竞品存在更多可改善空间；限定在合理评分区间
df["Improvement_Potential_Score"] = (
    ((4.5 - df["Average_Rating"]).clip(lower=0, upper=0.7) / 0.7) * 10
).round(1)

df["Initial_Screening_Score"] = (
    df["Demand_Score"]
    + df["Trend_Score"]
    + df["Competition_Score"]
    + df["Margin_Score"]
    + df["Improvement_Potential_Score"]
).round(1)

df["Initial_Screening_Result"] = df.apply(
    lambda row: (
        "Pass"
        if row[["Pass_Sales", "Pass_Trend", "Pass_Competition", "Pass_Margin"]].all()
        else "Hold"
    ),
    axis=1,
)

df = df.sort_values(
    by="Initial_Screening_Score",
    ascending=False
)

result_columns = [
    "Product_ID",
    "Product_Name",
    "Estimated_Monthly_Sales",
    "Search_Trend_Growth_Pct",
    "Estimated_Competitor_Count",
    "Estimated_Gross_Margin_Pct",
    "Average_Rating",
    "Initial_Screening_Score",
    "Initial_Screening_Result",
]

df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("\n=== 初筛结果 ===")
print(df[result_columns].to_string(index=False))
print(f"\n已生成：{OUTPUT_FILE.name}")
