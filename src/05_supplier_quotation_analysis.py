from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
CANDIDATE_FILE = ROOT_DIR / "data" / "raw" / "candidate_products_2.csv"
SUPPLIER_FILE = ROOT_DIR / "data" / "raw" / "supplier_quotations_4.csv"

DETAIL_OUTPUT_FILE = ROOT_DIR / "data" / "processed" / "supplier_quotation_analysis.csv"
SUMMARY_OUTPUT_FILE = ROOT_DIR / "data" / "processed" / "supplier_recommendation_summary.csv"

candidates = pd.read_csv(CANDIDATE_FILE)
suppliers = pd.read_csv(SUPPLIER_FILE)

# 1. 数据质量检查：每个产品必须有 2 家供应商
supplier_count_check = suppliers.groupby("Product_ID")["Supplier_ID"].nunique()

if not (supplier_count_check == 2).all():
    raise ValueError("供应商数据异常：请确认每个候选产品都有 2 家不同供应商。")

if not suppliers["Product_ID"].isin(candidates["Product_ID"]).all():
    raise ValueError("供应商数据中存在未在候选产品表出现的 Product_ID。")

# 2. 合并候选产品信息
suppliers = suppliers.merge(
    candidates[
        ["Product_ID", "Product_Name", "Estimated_COGS_USD"]
    ],
    on="Product_ID",
    how="left"
)

# 3. 计算报价与原始预估成本的差异
suppliers["Quote_vs_Estimated_COGS_Difference_USD"] = (
    suppliers["Unit_Quote_USD"] - suppliers["Estimated_COGS_USD"]
).round(2)

suppliers["Initial_Order_Value_USD"] = (
    suppliers["Unit_Quote_USD"] * suppliers["MOQ_Units"]
).round(2)

# 4. 供应商评分：同一个产品内比较
suppliers["Price_Score"] = (
    suppliers.groupby("Product_ID")["Unit_Quote_USD"].transform("min")
    / suppliers["Unit_Quote_USD"] * 30
).round(1)

suppliers["MOQ_Score"] = (
    suppliers.groupby("Product_ID")["MOQ_Units"].transform("min")
    / suppliers["MOQ_Units"] * 20
).round(1)

suppliers["Lead_Time_Score"] = (
    suppliers.groupby("Product_ID")["Mass_Production_Lead_Time_Days"].transform("min")
    / suppliers["Mass_Production_Lead_Time_Days"] * 20
).round(1)

suppliers["Quality_Score"] = (
    suppliers["Estimated_Quality_Score_100"] / 100 * 20
).round(1)

suppliers["Customization_Score"] = suppliers[
    "Customization_Available"
].map({"Yes": 10, "No": 0})

if suppliers["Customization_Score"].isna().any():
    raise ValueError("Customization_Available 只能填写 Yes 或 No。")

suppliers["Supplier_Total_Score"] = (
    suppliers["Price_Score"]
    + suppliers["MOQ_Score"]
    + suppliers["Lead_Time_Score"]
    + suppliers["Quality_Score"]
    + suppliers["Customization_Score"]
).round(1)

suppliers["Supplier_Rank"] = suppliers.groupby("Product_ID")[
    "Supplier_Total_Score"
].rank(
    method="dense",
    ascending=False
).astype(int)

suppliers["Supplier_Recommendation"] = suppliers["Supplier_Rank"].apply(
    lambda rank: "Recommended for Sampling" if rank == 1 else "Backup Supplier"
)

suppliers = suppliers.sort_values(
    by=["Product_ID", "Supplier_Rank"]
)

suppliers.to_csv(DETAIL_OUTPUT_FILE, index=False, encoding="utf-8-sig")

# 5. 生成每个产品的推荐供应商汇总表
recommended_suppliers = suppliers[
    suppliers["Supplier_Rank"] == 1
][
    [
        "Product_ID",
        "Product_Name",
        "Supplier_ID",
        "Supplier_Name",
        "Unit_Quote_USD",
        "MOQ_Units",
        "Mass_Production_Lead_Time_Days",
        "Estimated_Quality_Score_100",
        "Customization_Available",
        "Initial_Order_Value_USD",
        "Supplier_Total_Score",
        "Supplier_Recommendation",
    ]
]

recommended_suppliers.to_csv(
    SUMMARY_OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("=== 供应商推荐结果 ===")
print(recommended_suppliers.to_string(index=False))
print(f"\n已生成：{DETAIL_OUTPUT_FILE.name}")
print(f"已生成：{SUMMARY_OUTPUT_FILE.name}")
