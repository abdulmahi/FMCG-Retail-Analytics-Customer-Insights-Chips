import pandas as pd
from datetime import timedelta, datetime
import matplotlib.pyplot as plt

#Load the data
transaction_data = pd.read_csv('QVI_transaction_data.csv')
customer_data = pd.read_csv('QVI_purchase_behaviour.csv')

# Examine transaction data
print(transaction_data.head())
print(transaction_data.info())

# Convert DATE column to a date format, 1899 because CSV and excel integer begins on 30 Dec 1899 
origin_date = datetime.strptime('1899-12-30', '%Y-%m-%d')
transaction_data['DATE'] = transaction_data['DATE'].apply(lambda x: origin_date + timedelta(days=x))

# Check the first few rows to confirm the change
# print(transaction_data.head())
# print(transaction_data.info())

# # Summary of PROD_NAME
# print(transaction_data['PROD_NAME'].unique())

# Split product names into individual words and explode the list
transaction_data['words'] = transaction_data['PROD_NAME'].str.split()
words_exploded = transaction_data.explode('words')

# Remove words with digits or special characters
words_filtered = words_exploded[~words_exploded['words'].str.contains(r'\d|[^a-zA-Z\s]')]

# Print the changed column
print(words_filtered[['PROD_NAME', 'words']])

# Count the frequency of each word and sort
word_counts = words_filtered['words'].value_counts().sort_values(ascending=False)

# print(word_counts)

# Create a new column 'SALSA' which is True if 'PROD_NAME' contains the word 'salsa', and False if not or if the row is null
transaction_data['SALSA'] = transaction_data['PROD_NAME'].str.contains('salsa', case=False, na=False)

# Filter out the salsa products, i.e., keep only rows where 'SALSA' is False
transaction_data = transaction_data[transaction_data['SALSA'] == False]

# Drop the SALSA column as it is no longer needed
transaction_data = transaction_data.drop(columns=['SALSA'])

transaction_data = transaction_data.drop(columns=['words'])

# Summarize the data to check for nulls and possible outliers
summary_statistics = transaction_data.describe()
print(summary_statistics)

#number of null values
null_values = transaction_data.isnull().sum()
print("Null values in each column:")
print(null_values)

# Filter the dataset to find the outlier where 200 packets of chips are bought since max value is 200
outlier_transactions = transaction_data[transaction_data['PROD_QTY'] == 200]
print("Transactions where 200 packets of chips are bought:")
print(outlier_transactions)

# Identify the customer who made the outlier transaction
outlier_customer = outlier_transactions['LYLTY_CARD_NBR'].iloc[0]

# Filter the dataset to see all transactions made by this customer
customer_transactions = transaction_data[transaction_data['LYLTY_CARD_NBR'] == outlier_customer]
print(f"All transactions made by the customer {outlier_customer}:")
print(customer_transactions)

#It looks like this customer has only had the two transactions over the year and is 
#not an ordinary retail customer. The customer might be buying chips for commercial 
#purposes instead. We'll remove this loyalty card number from further analysis.


transaction_data = transaction_data[transaction_data['LYLTY_CARD_NBR'] != outlier_customer]
Count_Outlier_transaction_data = transaction_data[transaction_data['LYLTY_CARD_NBR'] == outlier_customer]
print(f"Transactions of the customer {outlier_customer} after filtering:")
print(Count_Outlier_transaction_data)# we get empty data frame so the outlier transcations has been removed.

# Grouping by the DATE column and counting the number of transactions for each date helps us understand the daily transaction volume.
transaction_count_by_date = transaction_data.groupby('DATE').size().reset_index(name='transaction_count')

# Create a sequence of dates from 1 Jul 2018 to 30 Jun 2019
full_date_range = pd.date_range(start='2018-07-01', end='2019-06-30')

# Left join the full date range table with the transaction count table
#The how='left' argument ensures that all dates in full_date_range are included, even if they don't have corresponding transaction data.
full_transaction_data = pd.DataFrame({'DATE': full_date_range}).merge(transaction_count_by_date, on='DATE', how='left').fillna(0)

# Plot the transaction count over time
plt.figure(figsize=(14, 7))
plt.plot(full_transaction_data['DATE'], full_transaction_data['transaction_count'], marker='o')
plt.title('Transaction Count Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Transactions')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Filter the data for December 2018
december_data = full_transaction_data[(full_transaction_data['DATE'] >= '2018-12-01') & (full_transaction_data['DATE'] <= '2018-12-31')]

# Plot the transaction count for December 2018
plt.figure(figsize=(14, 7))
plt.plot(december_data['DATE'], december_data['transaction_count'], marker='o')
plt.title('Transaction Count in December 2018')
plt.xlabel('Date')
plt.ylabel('Number of Transactions')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Extract pack size from PROD_NAME
transaction_data['PACK_SIZE'] = transaction_data['PROD_NAME'].str.extract(r'(\d+)').astype(int)

# Check if the pack sizes look sensible
pack_size_summary = transaction_data.groupby('PACK_SIZE').size().reset_index(name='transaction_count')
print(pack_size_summary.sort_values(by='PACK_SIZE'))

# Plot a histogram of PACK_SIZE
plt.figure(figsize=(10, 6))
plt.hist(transaction_data['PACK_SIZE'], bins=range(0, 500, 10), edgecolor='black')
plt.title('Histogram of Pack Sizes')
plt.xlabel('Pack Size')
plt.ylabel('Number of Transactions')
plt.grid(True)
plt.show()

# Extract brand from PROD_NAME
# We make a column called BRAND in the transaction_data table and then we use fill
# str.split splits the product names based on found white spaces and then str[0] takes the first word of the splited product name
transaction_data['BRAND'] = transaction_data['PROD_NAME'].str.split().str[0]

# Check the extracted brand names
# reset_index converts the series(description and value format) into a table like format(data frame) and then we name the column 'transaction count'
brand_summary = transaction_data.groupby('BRAND').size().reset_index(name='transaction_count')
print(brand_summary.sort_values(by='transaction_count', ascending=False))

# Clean brand names change Red to RRD (left to right)
brand_replacements = {
    'Red': 'RRD',
    'Smith': 'Smiths',
    'Dorito': 'Doritos',
    'Woolworths': 'WW',
    'Infzns' : 'Infuzions'
}

transaction_data['BRAND'] = transaction_data['BRAND'].replace(brand_replacements)

# Check the cleaned brand names
cleaned_brand_summary = transaction_data.groupby('BRAND').size().reset_index(name='transaction_count')
print(cleaned_brand_summary.sort_values(by='transaction_count', ascending=False))

# Plot a histogram of transaction counts by brand
plt.figure(figsize=(14, 7))
transaction_data['BRAND'].value_counts().plot(kind='bar')
plt.title('Transaction Count by Brand')
plt.xlabel('Brand')
plt.ylabel('Number of Transactions')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

print(customer_data.describe(include='all'))

# Distributions of key columns
key_columns = ['LIFESTAGE', 'PREMIUM_CUSTOMER']

for column in key_columns:
    plt.figure(figsize=(10, 5))
    customer_data[column].value_counts().plot(kind='bar')
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Merge transaction data with customer data
merged_data = pd.merge(transaction_data, customer_data, on='LYLTY_CARD_NBR', how='left')

# Check the merged data
print("\nMerged Data Sample:")
print(merged_data.head())

# Check for missing customer details
missing_customer_details = merged_data.isnull().sum()
print("Missing customer details:")
print(missing_customer_details[missing_customer_details > 0])

# Save the merged dataset as a CSV file
merged_data.to_csv('QVI_cleaned_data.csv', index=False)

# print("Data exploration is now complete and the dataset has been saved as 'QVI_cleaned_data.csv'.")


