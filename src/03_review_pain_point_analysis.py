from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
CANDIDATE_FILE = ROOT_DIR / "data" / "raw" / "candidate_products_2.csv"
REVIEW_FILE = ROOT_DIR / "data" / "raw" / "review_pain_points_4.csv"

DETAIL_OUTPUT_FILE = ROOT_DIR / "data" / "processed" / "review_pain_point_analysis.csv"
SUMMARY_OUTPUT_FILE = ROOT_DIR / "data" / "processed" / "product_improvement_summary.csv"

candidates = pd.read_csv(CANDIDATE_FILE)
reviews = pd.read_csv(REVIEW_FILE)
# 从候选产品表补充产品名称，供后续按产品汇总使用
reviews = reviews.merge(
    candidates[["Product_ID", "Product_Name"]],
    on="Product_ID",
    how="left"
)

# 1. 数据质量检查：每个产品必须有 2 条 Review 痛点
review_count_check = reviews.groupby("Product_ID")["Review_ID"].nunique()

if not (review_count_check == 2).all():
    raise ValueError("Review 数据异常：请确认每个候选产品都有 2 条痛点 Review。")

if not reviews["Product_ID"].isin(candidates["Product_ID"]).all():
    raise ValueError("Review 数据中存在未在候选产品表出现的 Product_ID。")

# 2. 将痛点严重程度转为可计算分数
severity_score_map = {
    "High": 3,
    "Medium": 2,
    "Low": 1,
}

reviews["Pain_Point_Severity_Score"] = reviews["Pain_Point_Severity"].map(
    severity_score_map
)

if reviews["Pain_Point_Severity_Score"].isna().any():
    raise ValueError("发现未定义的痛点严重程度，请检查 Pain_Point_Severity 字段。")

# 3. 按产品和严重程度排序，找出优先处理的痛点
reviews = reviews.sort_values(
    by=["Product_ID", "Pain_Point_Severity_Score", "Review_Rating"],
    ascending=[True, False, True]
)

# 保存逐条痛点分析
reviews.to_csv(DETAIL_OUTPUT_FILE, index=False, encoding="utf-8-sig")

# 4. 汇总每个产品的改进方向
summary = (
    reviews.groupby(["Product_ID", "Product_Name"])
    .agg(
        Pain_Point_Count=("Pain_Point_Category", "count"),
        Total_Pain_Point_Impact_Score=("Pain_Point_Severity_Score", "sum"),
        Highest_Severity_Score=("Pain_Point_Severity_Score", "max"),
        Priority_Pain_Point=("Pain_Point_Category", "first"),
        Recommended_Product_Upgrade=("Suggested_Product_Improvement", "first"),
    )
    .reset_index()
)

severity_label_map = {
    3: "High",
    2: "Medium",
    1: "Low",
}

summary["Highest_Severity"] = summary["Highest_Severity_Score"].map(
    severity_label_map
)

summary["Product_Improvement_Priority"] = summary[
    "Total_Pain_Point_Impact_Score"
].apply(
    lambda score: "High Priority" if score >= 5
    else "Medium Priority" if score >= 3
    else "Low Priority"
)

summary = summary.sort_values(
    by="Total_Pain_Point_Impact_Score",
    ascending=False
)

summary.to_csv(SUMMARY_OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("=== 产品痛点与改进方案 ===")
print(summary.to_string(index=False))
print(f"\n已生成：{DETAIL_OUTPUT_FILE.name}")
print(f"已生成：{SUMMARY_OUTPUT_FILE.name}")
