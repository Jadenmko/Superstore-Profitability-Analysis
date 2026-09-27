import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

#Reading xlsx file and seperating into three seperate dataframes by sheet
sheets = pd.read_excel('SuperStoreUS-2015.xlsx', sheet_name= None)
orders = sheets['Orders']
returns = sheets['Returns']
users = sheets["Users"]

#Cardinility check 
print(returns['Order ID'].duplicated().sum()) #0
print(orders['Region'].unique()) 
print(users['Region']) 
print(users['Region'].duplicated().sum()) #0

#left merge orders and returns
orders_returns = pd.merge(orders, returns, on= "Order ID", how = 'left')
print(orders_returns)
print(orders_returns['Status'].value_counts()) #15 from 1634 rows in returns, wery low match rate

returns_ids = set(returns['Order ID'])
orders_ids = set(orders['Order ID'])
print(len(returns_ids & orders_ids), "matched out of", len(returns_ids), "in Returns") #11 out of 1634

print(orders['Order ID'].nunique())
print(len(orders)) #587 duplicate order ids

#Merging left orders_returns with users
orders_returns_users = pd.merge(orders_returns, users, on= "Region", how= "left")
print(orders_returns_users)

sales_data = orders_returns_users.groupby(['Region', 'Product Category']).agg(
    Total_Sales = ('Sales', 'sum'), 
    Average_Sales = ('Sales', 'mean'), 
    Total_Profit = ('Profit', 'sum'),
    Unique_Orders = ('Order ID', 'nunique') 
    ).sort_values(by='Total_Sales', ascending= False).reset_index()

print(sales_data.head(12))

numeric_data = orders_returns_users[['Sales', 'Profit', 'Discount', 'Unit Price', 'Shipping Cost', 'Quantity ordered new']]
print(numeric_data)
print(numeric_data.describe())

corr_data = numeric_data.corr(method= 'spearman')
print(corr_data)

print(orders_returns_users.nsmallest(10, 'Profit')[['Region','Product Category','Unit Price','Discount','Profit', 'Sales', 'Quantity ordered new', 'Shipping Cost', 'Product Base Margin', 'Product Name']])

"""Making Bar Chart"""
sales_data_sorted = sales_data.sort_values(by= 'Total_Profit', ascending=False)
bar_series = sales_data_sorted['Region'] + '\n' + sales_data_sorted['Product Category']
bar_categories = bar_series.tolist()

bar_colors = ['green' if val > 0 else 'red' for val in sales_data_sorted['Total_Profit']]

plt.figure(figsize=(15, 6))
plt.bar(bar_categories, sales_data_sorted['Total_Profit'], color= bar_colors, edgecolor= 'black')

plt.axhline(0, color='black', linewidth= 1.2)

plt.ylabel('Total Profit / Loss ($)')
plt.title("Total Profit by Region and Product Category")
plt.xticks(fontsize=8)

plt.savefig('Profit_Region&Category.png', dpi= 300, bbox_inches='tight')

"""Making Scatter Diagram"""
plt.figure(figsize=(10, 8))
plt.scatter(numeric_data['Unit Price'], numeric_data['Profit'], edgecolors= 'black', color= 'blue')

plt.xscale('log')
plt.yscale('symlog', linthresh=10)

ax = plt.gca()
formatter = ScalarFormatter()
formatter.set_scientific(False)
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)

plt.ylabel('Profit($)')
plt.xlabel('Unit Price($)')
plt.title("Profit by Unit Price")

plt.savefig('Profit_UnitPrice.png', dpi= 300, bbox_inches='tight')
plt.show()







