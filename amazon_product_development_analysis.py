from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
OUTPUT_DIR = ROOT_DIR / "output"
REPORT_FILE = OUTPUT_DIR / "Amazon_Product_Development_Report.xlsx"


REPORT_SHEETS = {
    "Final Ranking": "05_final_product_opportunity_ranking.csv",
    "Initial Screening": "00_initial_screening_result.csv",
    "Competition": "01_competitor_analysis_summary.csv",
    "Review Insights": "02_product_improvement_summary.csv",
    "Keyword Analysis": "03_keyword_analysis_summary.csv",
    "Supplier Selection": "04_supplier_recommendation_summary.csv",
}


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    missing_files = [
        filename
        for filename in REPORT_SHEETS.values()
        if not (PROCESSED_DIR / filename).exists()
    ]
    if missing_files:
        missing_list = "\n".join(f"- {filename}" for filename in missing_files)
        raise FileNotFoundError(
            "缺少已处理数据文件，请先运行分阶段分析脚本：\n" + missing_list
        )

    with pd.ExcelWriter(REPORT_FILE, engine="openpyxl") as writer:
        for sheet_name, filename in REPORT_SHEETS.items():
            dataframe = pd.read_csv(PROCESSED_DIR / filename)
            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

            worksheet = writer.sheets[sheet_name]
            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions

            for column_cells in worksheet.columns:
                max_length = max(
                    len(str(cell.value)) if cell.value is not None else 0
                    for cell in column_cells
                )
                worksheet.column_dimensions[column_cells[0].column_letter].width = min(
                    max_length + 2, 35
                )

    print(f"Excel report created: {REPORT_FILE}")


if __name__ == "__main__":
    main()
