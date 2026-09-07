# Amazon Product Development Analysis

> 基于 Python 和 Pandas 构建的 Amazon US 家居收纳新品开发全流程模拟项目。

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-orange)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-Learning%20Project-lightgrey)](#免责声明)

## 一、项目简介

本项目模拟 Amazon 产品开发助理的基础工作流程：从候选产品池出发，完成产品初筛、竞品分析、Review 痛点分析、关键词分析、供应商报价比较，并通过机会评分选择优先开发的产品。

项目使用 2 个候选产品的精简模拟数据集，重点展示完整的数据关联、分析逻辑和产品开发决策过程。

> **数据说明：** 本项目的产品、竞品、关键词、供应商报价与上市表现均为模拟学习数据，不代表真实 Amazon 市场、卖家后台、品牌或供应商信息。

## 二、项目流程

```text
模拟候选产品数据
        ↓
产品初筛
        ↓
竞品价格、评分、评论与销量对比
        ↓
Review 痛点与产品改进方案
        ↓
关键词需求、趋势、竞争和广告成本分析
        ↓
供应商报价、MOQ、交期、质量与定制能力比较
        ↓
产品机会评分与开发优先级排序
        ↓
Excel 汇总报告
```

## 三、项目目录结构

```text
Amazon-Product-Development-Analysis
│
├── README.md
├── requirements.txt
├── amazon_product_development_analysis.py
│
├── src/
│   ├── 00_generate_simulated_dataset.py
│   ├── 01_initial_screening.py
│   ├── 02_competitor_analysis.py
│   ├── 03_review_pain_point_analysis.py
│   ├── 04_keyword_analysis.py
│   ├── 05_supplier_quotation_analysis.py
│   └── 06_opportunity_scoring.py
│
├── data/
│   ├── raw/
│   │   ├── candidate_products_2.csv
│   │   ├── competitor_data_4.csv
│   │   ├── review_pain_points_4.csv
│   │   ├── keyword_data_6.csv
│   │   ├── supplier_quotations_4.csv
│   │   └── launch_performance_last_month_2.csv
│   │
│   └── processed/
│       ├── initial_screening_result.csv
│       ├── competitor_analysis_summary.csv
│       ├── review_pain_point_analysis.csv
│       ├── product_improvement_summary.csv
│       ├── keyword_analysis_detail.csv
│       ├── keyword_analysis_summary.csv
│       ├── supplier_quotation_analysis.csv
│       ├── supplier_recommendation_summary.csv
│       └── final_product_opportunity_ranking.csv
│
└── output/
    └── Amazon_Product_Development_Report.xlsx
```

## 四、核心分析内容

| 阶段 | 目的 | 主要输出 |
|---|---|---|
| 产品初筛 | 判断需求、趋势、竞争与利润是否符合基本条件 | `initial_screening_result.csv` |
| 竞品分析 | 比较价格、评分、评论壁垒和销量竞争 | `competitor_analysis_summary.csv` |
| Review 分析 | 找到用户未被满足的需求并形成改进方案 | `product_improvement_summary.csv` |
| 关键词分析 | 判断搜索需求、趋势、竞争和预估 CPC | `keyword_analysis_summary.csv` |
| 供应商分析 | 比较报价、MOQ、交期、质量与定制能力 | `supplier_recommendation_summary.csv` |
| 机会评分 | 对候选产品进行综合排序 | `final_product_opportunity_ranking.csv` |

## 五、最终机会评分

最终评分满分 100 分，由以下部分组成：

| 维度 | 权重 | 判断内容 |
|---|---:|---|
| 初筛得分 | 25% | 销量、趋势、竞争数量、毛利率 |
| 竞争机会 | 20% | 竞品评论壁垒与评分改进空间 |
| Review 痛点机会 | 20% | 用户痛点严重程度及产品改进可能性 |
| 关键词机会 | 20% | 搜索需求、趋势、竞争和预估 CPC |
| 供应商能力 | 15% | 报价、MOQ、交期、质量、定制能力 |

评分用于学习项目中的产品排序和决策展示，并非真实商业预测。

## 六、运行方法

### 1. 安装依赖

```bash
python -m pip install -r requirements.txt
```

### 2. 生成 Excel 汇总报告

```bash
python amazon_product_development_analysis.py
```

运行后可在 `output/` 文件夹查看 `Amazon_Product_Development_Report.xlsx`。

### 3. 重新执行分阶段分析（可选）

阶段脚本保存在 `src/`。如需重新从模拟数据开始执行，请按编号从 `00` 至 `06` 运行。

## 七、技术栈

| 技术 | 用途 |
|---|---|
| Python | 数据处理与自动化分析 |
| Pandas | CSV 读取、清洗、合并、计算和导出 |
| OpenPyXL | 生成多工作表 Excel 汇总报告 |
| Git / GitHub | 版本管理与求职作品展示 |

## 八、项目亮点

- 建立了候选产品、竞品、Review、关键词、供应商与上市表现之间的 `Product_ID` 数据关联。
- 将用户负面反馈转化为明确的产品改进方案。
- 用多维度加权评分替代只看销量的单一选品判断。
- 完成从原始模拟数据到产品开发优先级排序的基础闭环。

## 九、局限与后续优化

1. 当前所有数据均为模拟学习数据；
2. 未接入 Amazon SP-API、Helium 10、Keepa 或真实广告数据；
3. 当前仅使用 2 个候选产品，后续可扩展为 20 至 30 个候选产品；
4. 后续可加入真实采购运费、关税、仓储费、盈亏平衡 ACOS 与样品测试记录。

## 十、作者

**姓名：罗嘉乐**  
**求职方向：跨境电商产品开发助理 / Amazon 运营助理**

## 十一、免责声明

本项目仅用于个人学习、Python 数据分析实践及求职作品展示。所有数据均为模拟数据，不应视为真实市场研究、采购报价或商业决策依据。
