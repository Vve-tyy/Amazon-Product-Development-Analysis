from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
CANDIDATE_FILE = ROOT_DIR / "data" / "raw" / "candidate_products_2.csv"
COMPETITOR_FILE = ROOT_DIR / "data" / "raw" / "competitor_data_4.csv"
OUTPUT_FILE = ROOT_DIR / "data" / "processed" / "competitor_analysis_summary.csv"

candidates = pd.read_csv(CANDIDATE_FILE)
competitors = pd.read_csv(COMPETITOR_FILE)

# 1. 数据质量检查：每个候选产品必须对应 2 个竞品
competitor_count_check = competitors.groupby("Product_ID")["Competitor_ID"].nunique()

if not (competitor_count_check == 2).all():
    raise ValueError("竞品数据异常：请确认每个候选产品都有 2 个不同的竞品。")

# 2. 按候选产品汇总竞品数据
competitor_summary = (
    competitors.groupby("Product_ID")
    .agg(
        Avg_Competitor_Price_USD=("Competitor_Price_USD", "mean"),
        Avg_Competitor_Rating=("Competitor_Rating", "mean"),
        Avg_Competitor_Review_Count=("Competitor_Review_Count", "mean"),
        Avg_Competitor_Monthly_Sales=("Competitor_Estimated_Monthly_Sales", "mean"),
    )
    .reset_index()
)

# 3. 合并候选产品和竞品汇总数据
result = candidates[
    [
        "Product_ID",
        "Product_Name",
        "Target_Price_USD",
        "Average_Rating",
        "Estimated_Monthly_Sales",
        "Estimated_Review_Count",
    ]
].merge(competitor_summary, on="Product_ID", how="left")

# 4. 计算竞争差距
result["Price_Gap_Pct"] = (
    (result["Target_Price_USD"] - result["Avg_Competitor_Price_USD"])
    / result["Avg_Competitor_Price_USD"]
    * 100
).round(1)

result["Rating_Gap"] = (
    result["Average_Rating"] - result["Avg_Competitor_Rating"]
).round(2)

result["Review_Barrier_Ratio"] = (
    result["Avg_Competitor_Review_Count"]
    / result["Estimated_Review_Count"]
).round(2)

result["Sales_Competition_Ratio"] = (
    result["Avg_Competitor_Monthly_Sales"]
    / result["Estimated_Monthly_Sales"]
).round(2)

# 5. 给出初步竞争判断
def get_competition_conclusion(row):
    if row["Avg_Competitor_Review_Count"] >= 2000:
        return "High Review Barrier"
    if row["Rating_Gap"] <= -0.10:
        return "Product Improvement Opportunity"
    if row["Price_Gap_Pct"] <= -5:
        return "Price Advantage"
    return "Moderate Competition"

result["Competition_Conclusion"] = result.apply(
    get_competition_conclusion,
    axis=1
)

result = result.sort_values(
    by=["Competition_Conclusion", "Avg_Competitor_Monthly_Sales"],
    ascending=[True, False]
)

result.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("=== 竞品分析结果 ===")
print(result.to_string(index=False))
print(f"\n已生成：{OUTPUT_FILE.name}")
