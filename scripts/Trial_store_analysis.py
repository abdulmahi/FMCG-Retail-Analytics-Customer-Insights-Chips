# Data Wrangling
import numpy as np
import pandas as pd

# Visualization
import matplotlib.pyplot as plt

# Date Functionality
import matplotlib.dates as mdates

# Statistics
from scipy.stats import ttest_ind

# Remove Warnings
import warnings
warnings.filterwarnings("ignore")

# Load the data
df1 = pd.read_csv('QVI_cleaned_data.csv')

# Display the first few rows of the dataframe
print(df1.head())

# Display the number of missing values in each column
print(df1.isnull().sum())

# Create a month ID in format yyyymm
df1['YEARMONTH'] = [''.join(x.split('-')[0:2]) for x in df1.DATE]
df1['YEARMONTH'] = pd.to_numeric(df1['YEARMONTH'])

# Total Sales for each store and month
Total_Sales = df1.groupby(['STORE_NBR', 'YEARMONTH']).TOT_SALES.sum()

# Number of customers for each store and month
no_Customers = df1.groupby(['STORE_NBR', 'YEARMONTH']).LYLTY_CARD_NBR.nunique()

# Transactions per customer for each store and month
trans_per_customer = df1.groupby(['STORE_NBR', 'YEARMONTH']).TXN_ID.nunique() / df1.groupby(['STORE_NBR', 'YEARMONTH']).LYLTY_CARD_NBR.nunique()

# Chips per customer for each store and month
chips_per_customer = df1.groupby(['STORE_NBR', 'YEARMONTH']).PROD_QTY.sum() / df1.groupby(['STORE_NBR', 'YEARMONTH']).TXN_ID.nunique()

# Average price per unit for each store and month
average_price = df1.groupby(['STORE_NBR', 'YEARMONTH']).TOT_SALES.sum() / df1.groupby(['STORE_NBR', 'YEARMONTH']).PROD_QTY.sum()

# Concatenate into a new dataframe 'measureOverTime'
df2 = [Total_Sales, no_Customers, trans_per_customer, chips_per_customer, average_price]
measureOverTime = pd.concat(df2, join='outer', axis=1)

# Rename the columns
measureOverTime.rename(columns={
    'TOT_SALES': 'Total Sales',
    'LYLTY_CARD_NBR': 'no_Customers',
    0: 'trans_per_customer',
    1: 'chips_per_customer',
    2: 'average_price'
}, inplace=True)

# Display the first 15 rows of the dataframe
print(measureOverTime.head(15))

# Reset the index of the dataframe
measureOverTime.reset_index(inplace=True)

# Display the updated dataframe
print(measureOverTime)

# Create a pivot table to check for full observation periods
df3 = pd.pivot_table(df1, index='STORE_NBR', columns='YEARMONTH', values='TXN_ID', aggfunc='count')

# Store numbers that do not have full observation periods
null_stores = df3[df3.isnull().any(axis=1)].index.tolist()

# Filter out the null stores
measureOverTime = measureOverTime[~measureOverTime['STORE_NBR'].isin(null_stores)]

# Display the updated dataframe
print(measureOverTime)

# Filter to pre-trial period before 201902
preTrialMeasures = measureOverTime[measureOverTime['YEARMONTH'] < 201902]

# Display the pre-trial measures
print(preTrialMeasures)

# Define function to calculate correlation for a measure
def calculateCorrelation(inputTable, metricCol, trial_store):
    calcCorrTable = []
    x = inputTable.loc[inputTable['STORE_NBR'] == trial_store, metricCol]
    x.reset_index(drop=True, inplace=True)
    storeNumbers = inputTable['STORE_NBR'].unique()
    for i in storeNumbers:
        y = inputTable.loc[inputTable['STORE_NBR'] == i, metricCol]
        y.reset_index(drop=True, inplace=True)
        calcCorrTable.append({'Store1': trial_store, 'Store2': i, 'corr_measure': y.corr(x)})
    return pd.DataFrame(calcCorrTable)

# Define function to calculate magnitude distance for a measure
def calculateMagnitudeDistance(inputTable, metricCol, trial_store):
    calcDistTable = []
    x = inputTable.loc[inputTable['STORE_NBR'] == trial_store, metricCol]
    x.reset_index(drop=True, inplace=True)
    storeNumbers = inputTable['STORE_NBR'].unique()
    for i in storeNumbers:
        y = inputTable.loc[inputTable['STORE_NBR'] == i, metricCol]
        y.reset_index(drop=True, inplace=True)
        z = abs(x - y)
        A = np.mean(1 - (z - min(z)) / (max(z) - min(z)))
        calcDistTable.append({'Store1': trial_store, 'Store2': i, 'Magnitude': A})
    return pd.DataFrame(calcDistTable)

# Function to find the most similar control store for a given trial store
# Function to find the most similar control store for a given trial store
# Function to find the most similar control store for a given trial store
def find_similar_control_store(preTrialMeasures, trial_store):
    corr_Sales = calculateCorrelation(preTrialMeasures, 'Total Sales', trial_store)
    corr_Customers = calculateCorrelation(preTrialMeasures, 'no_Customers', trial_store)

    magnitude_Sales = calculateMagnitudeDistance(preTrialMeasures, 'Total Sales', trial_store)
    magnitude_Customers = calculateMagnitudeDistance(preTrialMeasures, 'no_Customers', trial_store)

    # Combine correlation and magnitude scores
    score_Sales = pd.concat([corr_Sales, magnitude_Sales['Magnitude']], axis=1)
    score_Customers = pd.concat([corr_Customers, magnitude_Customers['Magnitude']], axis=1)

    # Add an additional column which calculates the weighted average
    corr_weight = 0.5
    score_Sales['scoreSales'] = corr_weight * score_Sales['corr_measure'] + (1 - corr_weight) * score_Sales['Magnitude']
    score_Customers['scoreCustomers'] = corr_weight * score_Customers['corr_measure'] + (1 - corr_weight) * score_Customers['Magnitude']

    # Set index for easier merging
    score_Sales.set_index(['Store1', 'Store2'], inplace=True)
    score_Customers.set_index(['Store1', 'Store2'], inplace=True)

    # Combine Sales and Customers scores into one dataframe
    score_Control = pd.concat([score_Sales['scoreSales'], score_Customers['scoreCustomers']], axis=1)

    # Add a new column 'finalControlScore' to 'score_Control'
    score_Control['finalControlScore'] = 0.5 * (score_Control['scoreSales'] + score_Control['scoreCustomers'])

    return score_Control.sort_values(by='finalControlScore', ascending=False).head()

# Define the trial stores
trial_stores = [77, 86, 88]

# Loop through each trial store and create visualizations
for trial_store in trial_stores:
    similar_control_stores = find_similar_control_store(preTrialMeasures, trial_store)

    # Create a grouped bar chart for correlation scores
    fig, ax = plt.subplots(figsize=(12, 8))
    width = 0.35  # Width of the bars

    store_indices = np.arange(len(similar_control_stores))
    
    bars1 = ax.bar(store_indices - width/2, similar_control_stores['scoreSales'], width, label='Sales Correlation')
    bars2 = ax.bar(store_indices + width/2, similar_control_stores['scoreCustomers'], width, label='Customer Correlation')
    
    ax.set_xlabel('Store Number')
    ax.set_ylabel('Correlation Score')
    ax.set_title(f'Top Control stores with highest Correlation/Similarity Scores against Trial Store {trial_store}')
    ax.set_xticks(store_indices)
    ax.set_xticklabels(similar_control_stores.index.get_level_values('Store2'))
    ax.legend()

# We find that the most similar stores for the trial stores 77, 86 and 88 are store 233, 155 and 14
# Now I will visualize the total sales and total customer metrics of these stores compared to the baseline others stores

# Function to visualize the metrics
def visualize_metrics(trial_store, control_store, preTrialMeasures):
    pastSales = preTrialMeasures.copy()
    store_type = []

    for i in pastSales['STORE_NBR']:
        if i == trial_store:
            store_type.append('Trial Store')
        elif i == control_store:
            store_type.append('Control Store')
        else:
            store_type.append('Other Stores')

    pastSales['store_type'] = store_type
    pastSales['TransactionMonth'] = pd.to_datetime(pastSales['YEARMONTH'].astype(str), format='%Y%m')
    pastSales['Month'] = pd.DatetimeIndex(pastSales['TransactionMonth']).month_name().str[:3]

    controlPlot = pastSales.loc[pastSales['store_type'] == 'Control Store', ['Month', 'Total Sales']]
    controlPlot.set_index('Month', inplace=True)

    trialPlot = pastSales.loc[pastSales['store_type'] == 'Trial Store', ['Month', 'Total Sales']]
    trialPlot.set_index('Month', inplace=True)

    otherPlot = pastSales.loc[pastSales['store_type'] == 'Other Stores', ['Month', 'Total Sales']]
    otherPlot = pd.DataFrame(otherPlot.groupby('Month')['Total Sales'].mean())

    # Renaming Column Names
    controlPlot.rename(columns={'Total Sales': 'Control Store Sales'}, inplace=True)
    trialPlot.rename(columns={'Total Sales': 'Trial Store Sales'}, inplace=True)
    otherPlot.rename(columns={'Total Sales': 'Other Stores Sales'}, inplace=True)

    # Concatenate
    combinePlot = pd.concat([controlPlot, trialPlot, otherPlot], axis=1)

    # Plot Total Sales
    combinePlot.plot(kind='line', figsize=(14, 8))
    plt.title(f'Total Sales Comparison for Trial Store {trial_store} and Control Store {control_store}')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.legend()
    plt.show()

    # Visualize total store customers
    controlPlot_customers = pastSales.loc[pastSales['store_type'] == 'Control Store', ['Month', 'no_Customers']]
    controlPlot_customers.set_index('Month', inplace=True)

    trialPlot_customers = pastSales.loc[pastSales['store_type'] == 'Trial Store', ['Month', 'no_Customers']]
    trialPlot_customers.set_index('Month', inplace=True)

    otherPlot_customers = pastSales.loc[pastSales['store_type'] == 'Other Stores', ['Month', 'no_Customers']]
    otherPlot_customers = pd.DataFrame(otherPlot_customers.groupby('Month')['no_Customers'].mean())

    # Renaming Column Names
    controlPlot_customers.rename(columns={'no_Customers': 'Control Store Customers'}, inplace=True)
    trialPlot_customers.rename(columns={'no_Customers': 'Trial Store Customers'}, inplace=True)
    otherPlot_customers.rename(columns={'no_Customers': 'Other Stores Customers'}, inplace=True)

    # Concatenate
    combinePlot_customers = pd.concat([controlPlot_customers, trialPlot_customers, otherPlot_customers], axis=1)

    # Plot Total Customers
    combinePlot_customers.plot(kind='line', figsize=(14, 8))
    plt.title(f'Total Customers Comparison for Trial Store {trial_store} and Control Store {control_store}')
    plt.xlabel('Month')
    plt.ylabel('Total Customers')
    plt.legend()
    plt.show()

# Define the trial stores and their most similar control stores
trial_control_pairs = {
    77: 233,
    86: 155,
    88: 14
}

# Visualize the metrics for each trial and control pair
for trial_store, control_store in trial_control_pairs.items():
    visualize_metrics(trial_store, control_store, preTrialMeasures)

# Function to assess the trial period
def assess_trial(trial_store, control_store, trial_period, measureOverTime):
    trial_data = measureOverTime[(measureOverTime['STORE_NBR'] == trial_store) & 
                                 (measureOverTime['YEARMONTH'] >= trial_period[0]) & 
                                 (measureOverTime['YEARMONTH'] <= trial_period[1])]
    
    control_data = measureOverTime[(measureOverTime['STORE_NBR'] == control_store) & 
                                   (measureOverTime['YEARMONTH'] >= trial_period[0]) & 
                                   (measureOverTime['YEARMONTH'] <= trial_period[1])]
    
    # Calculate total sales
    trial_total_sales = trial_data['Total Sales'].sum()
    control_total_sales = control_data['Total Sales'].sum()
    
    # Perform t-test to check if the difference in total sales is significant
    t_stat_sales, p_value_sales = ttest_ind(trial_data['Total Sales'], control_data['Total Sales'])
    
    # Calculate total customers
    trial_total_customers = trial_data['no_Customers'].sum()
    control_total_customers = control_data['no_Customers'].sum()
    
    # Perform t-test to check if the difference in number of customers is significant
    t_stat_customers, p_value_customers = ttest_ind(trial_data['no_Customers'], control_data['no_Customers'])
    
    print(f"Assessment for Trial Store {trial_store} and Control Store {control_store} during Trial Period:")
    print(f"Total Sales - Trial: {trial_total_sales}, Control: {control_total_sales}")
    print(f"T-test p-value for Total Sales: {p_value_sales}")
    
    if p_value_sales < 0.05:
        print("Significant difference in total sales during the trial period.")
    else:
        print("No significant difference in total sales during the trial period.")
    
    print(f"Total Customers - Trial: {trial_total_customers}, Control: {control_total_customers}")
    print(f"T-test p-value for Total Customers: {p_value_customers}")
    
    if p_value_customers < 0.05:
        print("Significant difference in number of customers during the trial period.")
    else:
        print("No significant difference in number of customers during the trial period.")
    
    print("\n")

# Define the trial period (example: February 2019 to April 2019)
trial_period = (201902, 201904)

# Assess the trial for each trial and control pair
for trial_store, control_store in trial_control_pairs.items():
    assess_trial(trial_store, control_store, trial_period, measureOverTime)

# Assessment for Trial Store 77 and Control Store 233 during Trial Period:
# Total Sales - Trial: 724.8, Control: 545.5
# T-test p-value for Total Sales: 0.08891766389958788
# No significant difference in total sales during the trial period.
# Total Customers - Trial: 133, Control: 104
# T-test p-value for Total Customers: 0.11721891203030974
# No significant difference in number of customers during the trial period.


# Assessment for Trial Store 86 and Control Store 155 during Trial Period:
# Total Sales - Trial: 2622.2, Control: 2418.2
# T-test p-value for Total Sales: 0.2258212492080038
# No significant difference in total sales during the trial period.
# Total Customers - Trial: 312, Control: 276
# T-test p-value for Total Customers: 0.011410571669866972
# Significant difference in number of customers during the trial period.


# Assessment for Trial Store 88 and Control Store 14 during Trial Period:
# Total Sales - Trial: 4123.6, Control: 64.89999999999999
# T-test p-value for Total Sales: 8.773245654055929e-06
# Significant difference in total sales during the trial period.
# Total Customers - Trial: 374, Control: 10
# T-test p-value for Total Customers: 9.793497825729776e-06
# Significant difference in number of customers during the trial period.