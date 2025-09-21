import pandas as pd
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns


#Load the data
merged_clean_data = pd.read_csv('QVI_cleaned_data.csv')

# Total sales by LIFESTAGE and PREMIUM_CUSTOMER
total_sales = merged_clean_data.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['TOT_SALES'].sum().reset_index()

plt.rcParams["figure.figsize"] = (18, 10)
plt.xticks(rotation=45)
sns.set_theme(style="whitegrid")
sns.barplot(x='LIFESTAGE', y='TOT_SALES', hue='PREMIUM_CUSTOMER', data=total_sales, ci=None)
plt.title('Total Sales by LIFESTAGE and PREMIUM_CUSTOMER')
plt.xlabel('LIFESTAGE')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.legend(title='PREMIUM_CUSTOMER', loc='upper right')
plt.tight_layout()
plt.show()

# Number of customers by LIFESTAGE and PREMIUM_CUSTOMER
# total_customer= merged_clean_data.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['LYLTY_CARD_NBR'].count().reset_index()
# total_customer_AVG= merged_clean_data.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['PROD_QTY'].mean().reset_index()

merged_clean_data['PRICE_PER_UNIT'] = merged_clean_data['TOT_SALES'] / merged_clean_data['PROD_QTY']
total_avg_price_per_unit = merged_clean_data.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['PRICE_PER_UNIT'].mean().reset_index()
# total_customer_by_lifestyle= total_customer.groupby(['LIFESTAGE']).sum().reset_index()
# total_customer_by_premium= total_customer.groupby(['PREMIUM_CUSTOMER']).sum().reset_index()
# Pivot the DataFrame for plotting
# Set plot size
# Plotting the total average price per unit
# Calculate average units sold
average_units_sold = merged_clean_data.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER'])['PROD_QTY'].mean().reset_index()

# Set plot size and theme
plt.rcParams["figure.figsize"] = (18, 10)
sns.set_theme(style="whitegrid")
sns.barplot(x='LIFESTAGE', y='PROD_QTY', hue='PREMIUM_CUSTOMER', data=average_units_sold, ci=None)
plt.title('Average Units Sold by LIFESTAGE and PREMIUM_CUSTOMER')
plt.xlabel('LIFESTAGE')
plt.ylabel('Average Units Sold')
plt.xticks(rotation=45)
plt.legend(title='PREMIUM_CUSTOMER', loc='upper right')
plt.tight_layout()
plt.show()

# Separate data for the different customer segments
mainstream = merged_clean_data[(merged_clean_data['PREMIUM_CUSTOMER'] == 'Mainstream') & 
                               (merged_clean_data['LIFESTAGE'].isin(['MIDAGE SINGLES/COUPLES', 'YOUNG SINGLES/COUPLES']))]

premium = merged_clean_data[(merged_clean_data['PREMIUM_CUSTOMER'] == 'Premium') & 
                            (merged_clean_data['LIFESTAGE'].isin(['MIDAGE SINGLES/COUPLES', 'YOUNG SINGLES/COUPLES']))]

budget = merged_clean_data[(merged_clean_data['PREMIUM_CUSTOMER'] == 'Budget') & 
                           (merged_clean_data['LIFESTAGE'].isin(['MIDAGE SINGLES/COUPLES', 'YOUNG SINGLES/COUPLES']))]

# Perform independent t-tests
t_stat_mainstream_vs_premium, p_value_mainstream_vs_premium = stats.ttest_ind(
    mainstream['PRICE_PER_UNIT'], premium['PRICE_PER_UNIT'], equal_var=False)

t_stat_mainstream_vs_budget, p_value_mainstream_vs_budget = stats.ttest_ind(
    mainstream['PRICE_PER_UNIT'], budget['PRICE_PER_UNIT'], equal_var=False)

# Print the results
print("Mainstream vs Premium:")
print(f"T-statistic: {t_stat_mainstream_vs_premium}, P-value: {p_value_mainstream_vs_premium}")

#T-statistic is 28.34 standard errors away from zero which is a very large value, suggesting a substantial difference between the two groups.
#The p-value is extremely small (much smaller than 0.05), indicating that the difference between the Mainstream and Premium segments is statistically significant. 
#This means there is strong evidence to reject the null hypothesis (which states that there is no difference in means between the two groups).

print("\nMainstream vs Budget:")
print(f"T-statistic: {t_stat_mainstream_vs_budget}, P-value: {p_value_mainstream_vs_budget}")

#difference in average price per unit between the Mainstream and Budget segments is 31.67 standard errors away from zero. 
#This is an even larger value, suggesting an even more substantial difference between the two groups.
#The p-value is extraordinarily small This means there is very strong evidence to reject the null hypothesis for this comparison as well.
#The large t-statistic values and extremely small p-values suggest that these differences are not due to random chance.

# Filter data for Mainstream - Young Singles/Couples
mainstream_young = merged_clean_data[(merged_clean_data['PREMIUM_CUSTOMER'] == 'Mainstream') & 
                                     (merged_clean_data['LIFESTAGE'] == 'YOUNG SINGLES/COUPLES')]

# Calculating the frequency of each brand
brand_preferences = mainstream_young['BRAND'].value_counts().reset_index()
brand_preferences.columns = ['BRAND', 'COUNT']
print("Brand preferences for Mainstream - Young Singles/Couples:")
print(brand_preferences)

# Plot the brand preferences
plt.figure(figsize=(10, 6))
sns.barplot(x='COUNT', y='BRAND', data=brand_preferences)
plt.title('Preferred Brands for Mainstream - Young Singles/Couples')
plt.xlabel('Count')
plt.ylabel('Brand')
plt.show()

#Seems like the Kettle brand is signficiantly more preferred by this group.

# Calculating the frequency of each pack size for the target segment
pack_size_preferences_target = mainstream_young['PACK_SIZE'].value_counts().reset_index()
pack_size_preferences_target.columns = ['PACK_SIZE', 'COUNT']

# Calculating the frequency of each pack size for the rest of the population
other_segments = merged_clean_data[~((merged_clean_data['PREMIUM_CUSTOMER'] == 'Mainstream') & 
                                     (merged_clean_data['LIFESTAGE'] == 'YOUNG SINGLES/COUPLES'))]
pack_size_preferences_other = other_segments['PACK_SIZE'].value_counts().reset_index()
pack_size_preferences_other.columns = ['PACK_SIZE', 'COUNT']

# Plot the pack size preferences
plt.figure(figsize=(10, 6))
sns.barplot(x='PACK_SIZE', y='COUNT', data=pack_size_preferences_target, color='blue', alpha=0.6, label='Mainstream - Young Singles/Couples')
sns.barplot(x='PACK_SIZE', y='COUNT', data=pack_size_preferences_other, color='red', alpha=0.6, label='Other Segments')
plt.title('Preferred Pack Sizes')
plt.xlabel('Pack Size')
plt.ylabel('Count')
plt.legend()
plt.show()

#The most preferred pack size for every group appears to be 175g, followed by 150g and 200g.
#The secondary preferences (150g and 200g) are also similar between the two groups, indicating a general consistency in pack size preferences among different customer segments.