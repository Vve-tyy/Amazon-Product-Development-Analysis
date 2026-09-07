from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
CANDIDATE_FILE = ROOT_DIR / "data" / "raw" / "candidate_products_2.csv"
KEYWORD_FILE = ROOT_DIR / "data" / "raw" / "keyword_data_6.csv"

DETAIL_OUTPUT_FILE = ROOT_DIR / "data" / "processed" / "keyword_analysis_detail.csv"
SUMMARY_OUTPUT_FILE = ROOT_DIR / "data" / "processed" / "keyword_analysis_summary.csv"

candidates = pd.read_csv(CANDIDATE_FILE)
keywords = pd.read_csv(KEYWORD_FILE)

# 1. 数据质量检查：每个产品必须有 3 个关键词
keyword_count_check = keywords.groupby("Product_ID")["Keyword_ID"].nunique()

if not (keyword_count_check == 3).all():
    raise ValueError("关键词数据异常：请确认每个候选产品都有 3 个不同关键词。")

if not keywords["Product_ID"].isin(candidates["Product_ID"]).all():
    raise ValueError("关键词数据中存在未在候选产品表出现的 Product_ID。")

# 2. 补充产品名称
keywords = keywords.merge(
    candidates[["Product_ID", "Product_Name"]],
    on="Product_ID",
    how="left"
)

# 3. 将关键词竞争度转为评分
competition_score_map = {
    "Low": 20,
    "Medium": 12,
    "High": 6,
}

keywords["Keyword_Competition_Score"] = keywords[
    "Keyword_Competition_Level"
].map(competition_score_map)

if keywords["Keyword_Competition_Score"].isna().any():
    raise ValueError("发现未定义的关键词竞争等级。")

# 保存关键词明细分析
keywords.to_csv(DETAIL_OUTPUT_FILE, index=False, encoding="utf-8-sig")

# 4. 汇总每个产品的关键词表现
summary = (
    keywords.groupby(["Product_ID", "Product_Name"])
    .agg(
        Keyword_Count=("Keyword_ID", "count"),
        Keyword_Search_Signal=("Monthly_Search_Volume", "sum"),
        Avg_Search_Trend_Growth_Pct=("Search_Trend_Growth_Pct", "mean"),
        Avg_Estimated_CPC_USD=("Estimated_CPC_USD", "mean"),
        Avg_Keyword_Competition_Score=("Keyword_Competition_Score", "mean"),
    )
    .reset_index()
)

# 5. 关键词机会评分：满分 100
summary["Search_Demand_Score"] = (
    summary["Keyword_Search_Signal"].clip(upper=40000) / 40000 * 40
).round(1)

summary["Keyword_Trend_Score"] = (
    summary["Avg_Search_Trend_Growth_Pct"].clip(upper=20) / 20 * 25
).round(1)

summary["Keyword_Competition_Score"] = (
    summary["Avg_Keyword_Competition_Score"] / 20 * 20
).round(1)

summary["CPC_Score"] = (
    ((2 - summary["Avg_Estimated_CPC_USD"]).clip(lower=0, upper=2) / 2 * 15)
).round(1)

summary["Keyword_Opportunity_Score"] = (
    summary["Search_Demand_Score"]
    + summary["Keyword_Trend_Score"]
    + summary["Keyword_Competition_Score"]
    + summary["CPC_Score"]
).round(1)

summary["Keyword_Opportunity_Conclusion"] = summary[
    "Keyword_Opportunity_Score"
].apply(
    lambda score: "High Keyword Opportunity" if score >= 70
    else "Medium Keyword Opportunity" if score >= 50
    else "Low Keyword Opportunity"
)

summary = summary.sort_values(
    by="Keyword_Opportunity_Score",
    ascending=False
)

summary.to_csv(SUMMARY_OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("=== 关键词分析结果 ===")
print(summary.to_string(index=False))
print(f"\n已生成：{DETAIL_OUTPUT_FILE.name}")
print(f"已生成：{SUMMARY_OUTPUT_FILE.name}")
