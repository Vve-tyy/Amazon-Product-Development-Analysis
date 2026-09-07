from pathlib import Path
import pandas as pd

# 全部内容均为模拟学习数据，不代表真实 Amazon 市场信息
DATA_FLAG = "SIMULATED_LEARNING_DATA"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

if not OUTPUT_DIR.exists():
    raise FileNotFoundError(f"请先创建文件夹：{OUTPUT_DIR}")

products = pd.DataFrame([
    {
        "Data_Flag": DATA_FLAG,
        "Product_ID": "P001",
        "Product_Name": "Under Sink Organizer",
        "Marketplace": "Amazon US",
        "Category": "Home & Kitchen",
        "Product_Segment": "Kitchen Storage",
        "Target_Price_USD": 29.99,
        "Estimated_Monthly_Sales": 3200,
        "Average_Rating": 4.2,
        "Estimated_Review_Count": 1850,
        "Main_Keyword_Search_Volume": 22000,
        "Search_Trend_Growth_Pct": 14.2,
        "Estimated_Competitor_Count": 65,
        "Estimated_COGS_USD": 7.80,
        "Estimated_FBA_Fee_USD": 7.20,
        "Estimated_Referral_Fee_USD": 4.50,
        "Estimated_Gross_Margin_Pct": 35.0,
        "Research_Status": "Pending Initial Screening",
    },
    {
        "Data_Flag": DATA_FLAG,
        "Product_ID": "P002",
        "Product_Name": "Shower Caddy Organizer",
        "Marketplace": "Amazon US",
        "Category": "Home & Kitchen",
        "Product_Segment": "Bathroom Organization",
        "Target_Price_USD": 28.99,
        "Estimated_Monthly_Sales": 2900,
        "Average_Rating": 4.1,
        "Estimated_Review_Count": 1420,
        "Main_Keyword_Search_Volume": 19500,
        "Search_Trend_Growth_Pct": 12.8,
        "Estimated_Competitor_Count": 79,
        "Estimated_COGS_USD": 7.20,
        "Estimated_FBA_Fee_USD": 7.00,
        "Estimated_Referral_Fee_USD": 4.35,
        "Estimated_Gross_Margin_Pct": 35.0,
        "Research_Status": "Pending Initial Screening",
    },
])

competitors = pd.DataFrame([
    [DATA_FLAG, "P001", "C001-1", "SpaceMax Under Sink Organizer", 27.99, 4.4, 2300, 3500, "Rust-resistant coating"],
    [DATA_FLAG, "P001", "C001-2", "HomePro Under Sink Organizer", 31.99, 4.2, 1800, 2900, "Tool-free assembly"],
    [DATA_FLAG, "P002", "C002-1", "Prime Shower Caddy Organizer", 26.99, 4.3, 2100, 3300, "Strong adhesive mounting"],
    [DATA_FLAG, "P002", "C002-2", "EasyNest Shower Caddy Organizer", 30.99, 4.0, 1350, 2500, "Large capacity design"],
], columns=[
    "Data_Flag", "Product_ID", "Competitor_ID", "Competitor_Name",
    "Competitor_Price_USD", "Competitor_Rating", "Competitor_Review_Count",
    "Competitor_Estimated_Monthly_Sales", "Main_Differentiation_Claim"
])

reviews = pd.DataFrame([
    [DATA_FLAG, "R001-1", "P001", "C001-1", 1, "Negative", "Rusting", "High",
     "Metal coating rusted after several weeks in a humid kitchen.",
     "Use thicker rust-resistant stainless steel with protective coating."],
    [DATA_FLAG, "R001-2", "P001", "C001-2", 2, "Negative", "Poor Stability", "High",
     "The organizer shifts when pulling out cleaning supplies.",
     "Add anti-slip feet and reinforced support structure."],
    [DATA_FLAG, "R002-1", "P002", "C002-1", 1, "Negative", "Weak Adhesive", "High",
     "Adhesive failed after being exposed to shower moisture.",
     "Use waterproof adhesive strips plus optional screw installation."],
    [DATA_FLAG, "R002-2", "P002", "C002-2", 2, "Negative", "Poor Drainage", "Medium",
     "Water collects at the bottom and is difficult to clean.",
     "Add drainage slots and a removable drip tray."],
], columns=[
    "Data_Flag", "Review_ID", "Product_ID", "Competitor_ID", "Review_Rating",
    "Review_Sentiment", "Pain_Point_Category", "Pain_Point_Severity",
    "Representative_Review_Summary", "Suggested_Product_Improvement"
])

keywords = pd.DataFrame([
    [DATA_FLAG, "K001-1", "P001", "under sink organizer", 22000, 14.2, 1.15, "High", "Core Purchase Intent"],
    [DATA_FLAG, "K001-2", "P001", "under sink storage", 9800, 11.0, 0.92, "Medium", "Feature Intent"],
    [DATA_FLAG, "K001-3", "P001", "kitchen cabinet organizer", 7600, 8.5, 0.88, "Medium", "Category Intent"],
    [DATA_FLAG, "K002-1", "P002", "shower caddy organizer", 19500, 12.8, 1.08, "High", "Core Purchase Intent"],
    [DATA_FLAG, "K002-2", "P002", "adhesive shower organizer", 8400, 16.3, 0.95, "Medium", "Feature Intent"],
    [DATA_FLAG, "K002-3", "P002", "bathroom shower shelf", 7100, 7.4, 0.82, "Medium", "Category Intent"],
], columns=[
    "Data_Flag", "Keyword_ID", "Product_ID", "Keyword", "Monthly_Search_Volume",
    "Search_Trend_Growth_Pct", "Estimated_CPC_USD",
    "Keyword_Competition_Level", "Search_Intent"
])

suppliers = pd.DataFrame([
    [DATA_FLAG, "Q001-1", "P001", "S001", "Simulated Supplier A", 7.50, 500, 95, 25, 88, "Yes", "Custom Color Box"],
    [DATA_FLAG, "Q001-2", "P001", "S002", "Simulated Supplier B", 8.10, 300, 110, 20, 84, "Yes", "Standard Box"],
    [DATA_FLAG, "Q002-1", "P002", "S003", "Simulated Supplier C", 6.90, 500, 90, 28, 90, "Yes", "Custom Color Box"],
    [DATA_FLAG, "Q002-2", "P002", "S004", "Simulated Supplier D", 7.40, 300, 105, 22, 85, "No", "Standard Box"],
], columns=[
    "Data_Flag", "Quotation_ID", "Product_ID", "Supplier_ID", "Supplier_Name",
    "Unit_Quote_USD", "MOQ_Units", "Sample_Fee_USD",
    "Mass_Production_Lead_Time_Days", "Estimated_Quality_Score_100",
    "Customization_Available", "Packaging_Option"
])

launch_performance = pd.DataFrame([
    [DATA_FLAG, "L001-202608", "P001", "2026-08", 1180, 35388.20, 5100.00, 12.6, 4.8, 4.3, "Healthy"],
    [DATA_FLAG, "L002-202608", "P002", "2026-08", 960, 27830.40, 4600.00, 11.8, 5.6, 4.2, "Healthy"],
], columns=[
    "Data_Flag", "Performance_ID", "Product_ID", "Performance_Month",
    "Units_Sold", "Revenue_USD", "Ad_Spend_USD", "Conversion_Rate_Pct",
    "Return_Rate_Pct", "Average_Rating", "Inventory_Health"
])

datasets = {
    "candidate_products_2.csv": products,
    "competitor_data_4.csv": competitors,
    "review_pain_points_4.csv": reviews,
    "keyword_data_6.csv": keywords,
    "supplier_quotations_4.csv": suppliers,
    "launch_performance_last_month_2.csv": launch_performance,
}

for filename, dataframe in datasets.items():
    dataframe.to_csv(OUTPUT_DIR / filename, index=False, encoding="utf-8-sig")
    print(f"Created {filename}: {len(dataframe)} rows")

print("完成：所有文件均为模拟学习数据。")
