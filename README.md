# FMCG Retail Analytics & Customer Insights (Chips Category)

This project analyses chip purchase behaviour from an FMCG retailer and evaluates the effectiveness of trial store layouts.  
It was completed as part of a structured analytics workflow using **Python, pandas, matplotlib, and scipy**.

---

## 📊 Project Overview
The analysis followed three stages:

1. **QVI Analysis (Initial Exploration)**  
   - Loaded transaction and customer datasets.  
   - Cleaned dates, handled missing values, and performed exploratory analysis.  

2. **Chip Analysis (Customer Insights)**  
   - Removed irrelevant products (e.g., salsa) and outliers.  
   - Extracted product attributes: **Pack Size** and **Brand**.  
   - Merged with customer segments (lifestage, premium).  
   - Analysed purchase behaviour by segment.  
   - Identified target segments and their brand/pack-size preferences.  

3. **Trial Store Analysis (Experiment Evaluation)**  
   - Defined trial stores (77, 86, 88) and selected control stores using correlation & magnitude similarity.  
   - Compared trial vs control stores on sales and customer numbers.  
   - Conducted t-tests to determine statistical significance.  
   - Concluded that Store 88’s trial was successful (uplift in both sales & customers).  

---

## 🎯 Objectives
- Explore and clean retail FMCG transaction data.  
- Understand customer behaviour by demographics and premium status.  
- Identify high-value customer segments and product preferences.  
- Evaluate the effectiveness of trial store layout changes using statistical testing.  

---

## ⚙️ Tools & Techniques
- **Python**: pandas, numpy, matplotlib, scipy  
- **Jupyter Notebook** for analysis and reporting  
- **Data cleaning & feature engineering** (regex, outlier detection, merging)  
- **Statistical testing** (independent t-tests)  
- **Experimental design** (trial vs control store evaluation)  

---


---

## 🚀 Key Insights
- **Segments:** Mainstream *Young/Midage Singles & Couples* are high-value customers.  
- **Products:** *Kettle* brand and **175g packs** dominate preferences → use as hero SKUs.  
- **Trial Results:**  
  - Store **88**: Successful trial (sales + customers uplift).  
  - Store **86**: Customer uplift only.  
  - Store **77**: Neutral impact.  

---

## 📄 Acknowledgement
This project is based on a retail analytics case study scenario (FMCG – chips category).  
It has been implemented independently in Python for learning and portfolio purposes.
