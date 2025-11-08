# 💄 Laneige TikTok Video Analytics Dashboard (June 2025)

This repository hosts an **interactive HTML dashboard** analyzing Laneige’s TikTok Shop performance for June 2025.  
It integrates video-level metrics, sampling cost estimation, and product-level ROI to uncover actionable insights that drive marketing efficiency and creative optimization.

---

## 📊 Overview

The dashboard visualizes **key performance indicators (KPIs)** from TikTok marketing and e-commerce campaigns, focusing on:

- **Video Performance** — reach, engagement, conversions, and gross merchandise value (GMV)  
- **Sampling Efficiency** — cost per mille (CPM) considering sampling and shipping costs  
- **Product Profitability** — revenue contribution and repeat-buyer analysis  
- **Regional Insights** — U.S. state-level GMV, repeat rates, and profitability

All visuals were built using **Plotly Dash** and exported as a single-file HTML for shareability.

---

## 🧮 Data & Calculation Framework

| Metric | Formula / Description |
|--------|-----------------------|
| **CPM (Cost per Mille)** | `CPM = (10 × sample_count + 0.15 × sample_value) ÷ views × 1000` |
| **Product Cost** | 15% of retail price + \$10 flat shipping fee |
| **Repeat Buyer Rate** | `repeat_buyer / total_buyer` |
| **ROI (Simplified)** | `(GMV - total_cost) / total_cost` |

All source data originated from TikTok Shop order exports (May–July 2025) and internal product sheets.

---

## 🧠 Key Insights (June 2025)

### 1️⃣ Video-Level Highlights
- Over **10,000 videos analyzed** (~353 per day)  
- **Average CPM:** \$2.87  
- High-performing creatives achieved **4–5× ROI** with balanced sample spending  
- Videos featuring *product close-ups* or *UGC tutorials* consistently outperform influencer ads  

### 2️⃣ Product Performance
| Rank | Product | % of Total Orders | Key Takeaway |
|------|----------|------------------|---------------|
| 🥇 1 | Glaze Craze Serum | 34.7% | Top GMV driver; strong organic conversion |
| 🥈 2 | Mini Lip Balm Set | 26.8% | High repeat-buyer rate (38%) |
| 🥉 3 | Bubble Tea Balm | 19.4% | Strong impulse-buy behavior |

Together, these top-3 SKUs contributed **80.9% of all orders**.

### 3️⃣ Regional & Buyer Insights
- **California, New York, and Texas** lead in GMV and repeat buyers  
- **Western U.S.** exhibits the highest profit margins  
- Sampling campaigns are most cost-effective in **densely populated metro states**

---

## 🧰 Tech Stack

- **Python**: `pandas`, `plotly`, `numpy`, `dash`, `argparse`  
- **Visualization**: Plotly Interactive HTML Export  
- **Data Source**: TikTok Shop Order Logs (May–July 2025)  
- **Dashboard Theme**: White background, blue accent, interactive tooltips, state-level drilldowns  

---

## 🚀 How to View

1. Clone the repository or download the HTML file:
   ```bash
   git clone https://github.com/Gavin-tian/TikTok_Laneige_Video_Analysis.git
   cd TikTok_Laneige_Video_Analysis
