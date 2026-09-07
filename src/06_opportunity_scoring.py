from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

candidates = pd.read_csv(RAW_DIR / "candidate_products_2.csv")
screening = pd.read_csv(PROCESSED_DIR / "initial_screening_result.csv")
competition = pd.read_csv(PROCESSED_DIR / "competitor_analysis_summary.csv")
review_summary = pd.read_csv(PROCESSED_DIR / "product_improvement_summary.csv")
keyword_summary = pd.read_csv(PROCESSED_DIR / "keyword_analysis_summary.csv")
supplier_summary = pd.read_csv(PROCESSED_DIR / "supplier_recommendation_summary.csv")

OUTPUT_FILE = PROCESSED_DIR / "final_product_opportunity_ranking.csv"


def check_product_coverage(dataframe, dataframe_name):
    candidate_ids = set(candidates["Product_ID"])
    dataframe_ids = set(dataframe["Product_ID"])

    if candidate_ids != dataframe_ids:
        raise ValueError(
            f"{dataframe_name} 的 Product_ID 与候选产品表不一致，请检查前面步骤的输出文件。"
        )


check_product_coverage(screening, "初筛结果")
check_product_coverage(competition, "竞品分析结果")
check_product_coverage(review_summary, "Review 痛点汇总")
check_product_coverage(keyword_summary, "关键词汇总")
check_product_coverage(supplier_summary, "供应商推荐结果")

# 1. 合并前面各阶段的关键指标
result = candidates[
    ["Product_ID", "Product_Name", "Target_Price_USD"]
].merge(
    screening[
        ["Product_ID", "Initial_Screening_Score", "Initial_Screening_Result"]
    ],
    on="Product_ID",
    how="left"
).merge(
    competition[
        [
            "Product_ID",
            "Avg_Competitor_Rating",
            "Avg_Competitor_Review_Count",
            "Price_Gap_Pct",
            "Rating_Gap",
        ]
    ],
    on="Product_ID",
    how="left"
).merge(
    review_summary[
        [
            "Product_ID",
            "Priority_Pain_Point",
            "Recommended_Product_Upgrade",
            "Total_Pain_Point_Impact_Score",
            "Product_Improvement_Priority",
        ]
    ],
    on="Product_ID",
    how="left"
).merge(
    keyword_summary[
        [
            "Product_ID",
            "Keyword_Opportunity_Score",
            "Keyword_Opportunity_Conclusion",
        ]
    ],
    on="Product_ID",
    how="left"
).merge(
    supplier_summary[
        [
            "Product_ID",
            "Supplier_Name",
            "Unit_Quote_USD",
            "MOQ_Units",
            "Supplier_Total_Score",
        ]
    ],
    on="Product_ID",
    how="left"
)

# 2. 计算竞争机会分，满分 20 分
# 竞品评论越少，新品进入时需要克服的评价壁垒越低
result["Review_Barrier_Score"] = (
    (3000 - result["Avg_Competitor_Review_Count"]).clip(lower=0, upper=3000)
    / 3000 * 10
).round(1)

# 竞品评分较低，说明用户体验可能仍有改进空间
result["Competitor_Rating_Opportunity_Score"] = (
    (4.5 - result["Avg_Competitor_Rating"]).clip(lower=0, upper=0.7)
    / 0.7 * 10
).round(1)

result["Competition_Opportunity_Score"] = (
    result["Review_Barrier_Score"]
    + result["Competitor_Rating_Opportunity_Score"]
).round(1)

# 3. 将 Review 痛点转化为开发机会分，满分 20 分
result["Pain_Point_Opportunity_Score"] = (
    result["Total_Pain_Point_Impact_Score"].clip(upper=6)
    / 6 * 20
).round(1)

# 4. 最终机会评分，满分 100 分
result["Final_Opportunity_Score"] = (
    result["Initial_Screening_Score"] * 0.25
    + result["Competition_Opportunity_Score"] * 0.20
    + result["Pain_Point_Opportunity_Score"] * 0.20
    + result["Keyword_Opportunity_Score"] * 0.20
    + result["Supplier_Total_Score"] * 0.15
).round(1)

result["Development_Rank"] = result["Final_Opportunity_Score"].rank(
    method="dense",
    ascending=False
).astype(int)

def get_development_recommendation(row):
    if (
        row["Development_Rank"] == 1
        and row["Initial_Screening_Result"] == "Pass"
        and row["Final_Opportunity_Score"] >= 45
    ):
        return "Priority Product for Development"
    if row["Final_Opportunity_Score"] >= 40:
        return "Keep as Backup Product"
    return "Do Not Prioritize"

result["Development_Recommendation"] = result.apply(
    get_development_recommendation,
    axis=1
)

result = result.sort_values(
    by="Development_Rank",
    ascending=True
)

result.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("=== 最终产品机会排名 ===")
print(result.to_string(index=False))
print(f"\n已生成：{OUTPUT_FILE.name}")
