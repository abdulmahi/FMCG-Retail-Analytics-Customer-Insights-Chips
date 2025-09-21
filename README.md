# FMCG Retail Analytics & Customer Insights (Chips Category)

This project analyses chip purchase behaviour from an FMCG retailer and evaluates the effectiveness of trial store layouts.  
It was completed as part of a structured analytics workflow using **Python, pandas, matplotlib, and scipy**.

---

## 🎯 Objectives
- Explore and clean transaction data & purchase behaviour data.  
- Understand customer behaviour by demographics and membership status.  
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

## 📂 Datasets
- **Transaction Data**:  
  Each row represents a customer transaction, including purchase date, store number, product name, quantity, and dollar sales.  

- **Purchase Behaviour Data**:  
  Customer-level demographics linked by loyalty card ID, including **Lifestage** (e.g., *Young Singles/Couples*, *Retirees*) and **Premium Membership Type** (*Premium, Mainstream, Budget*).  

- **Cleaned/Merged Data (QVI)**:  
  Output dataset after cleaning and joining the above. Includes engineered attributes like **Pack Size (grams)**, **Brand**, and **Price per Unit** for customer insights and statistical testing.  

---

## 📊 Process Overview
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

3. **Trial Store Analysis (Statistical Evaluation)**  
   - Defined trial stores (77, 86, 88) and selected control stores using **correlation & magnitude similarity**.  
   - Compared trial vs control stores on **sales** and **customer numbers**.  
   - Conducted **t-tests** to determine statistical significance.  

---


## 🚀 Key Insights  

- **Customer Segments**  
  - *Mainstream Young & Midage Singles/Couples* are the highest-value customers, driving strong chip sales.  
  - Premium shoppers pay more per unit, but growth opportunities lie in the Mainstream segment.  

- **Product Preferences**  
  - *Kettle* is the leading brand across target customers.  
  - **175g packs** dominate sales and should be used as “hero SKUs” for promotions.  

- **Trial Store Results**  
  - **Store 88** → Significant uplift in both sales and customer numbers → trial successful.  
  - **Store 86** → Increased customer traffic but limited sales uplift.  
  - **Store 77** → No meaningful change (neutral).  

📌 **Recommendation:** Prioritise marketing *175g Kettle products* to *Mainstream Young & Midage Singles/Couples*, and scale layout changes starting with stores similar to **Store 88**.  



