import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Load the data
df = pd.read_csv('BMW.csv')

print("=== BMW DATASET EXPLORATORY DATA ANALYSIS ===\n")

# 1. BASIC DATA OVERVIEW
print("1. BASIC DATA OVERVIEW")
print("=" * 50)
print(f"Dataset shape: {df.shape}")
print(f"Number of records: {df.shape[0]}")
print(f"Number of features: {df.shape[1]}\n")

print("First 5 rows:")
print(df.head())

print("\nDataset info:")
print(df.info())

print("\nBasic statistics:")
print(df.describe())

# 2. DATA QUALITY CHECK
print("\n2. DATA QUALITY CHECK")
print("=" * 50)
print("Missing values:")
missing_data = df.isnull().sum()
print(missing_data[missing_data > 0] if missing_data.any() else "No missing values!")

print("\nDuplicate rows:", df.duplicated().sum())

print("\nData types:")
print(df.dtypes)

# 3. UNIVARIATE ANALYSIS
print("\n3. UNIVARIATE ANALYSIS")
print("=" * 50)

# Categorical variables
categorical_cols = ['Model', 'Region', 'Color', 'Fuel_Type', 'Transmission', 'Sales_Classification']
print("\nCategorical Variables Analysis:")

fig, axes = plt.subplots(2, 3, figsize=(20, 12))
axes = axes.ravel()

for i, col in enumerate(categorical_cols):
    value_counts = df[col].value_counts()
    axes[i].bar(value_counts.index, value_counts.values)
    axes[i].set_title(f'{col} Distribution')
    axes[i].tick_params(axis='x', rotation=45)
    axes[i].set_ylabel('Count')
    
    # Add percentage labels
    total = len(df[col])
    for j, (category, count) in enumerate(value_counts.items()):
        axes[i].text(j, count + total*0.01, f'{count/total*100:.1f}%', 
                   ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Numerical variables
numerical_cols = ['Year', 'Engine_Size_L', 'Mileage_KM', 'Price_USD', 'Sales_Volume']
print("\nNumerical Variables Analysis:")

fig, axes = plt.subplots(2, 3, figsize=(20, 12))
axes = axes.ravel()

for i, col in enumerate(numerical_cols):
    # Histogram with KDE
    axes[i].hist(df[col], bins=30, alpha=0.7, density=True, edgecolor='black')
    df[col].plot.density(ax=axes[i], color='red', linewidth=2)
    axes[i].set_title(f'{col} Distribution')
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('Density')
    
    # Add statistics
    stats_text = f'Mean: {df[col].mean():.2f}\nStd: {df[col].std():.2f}\nMedian: {df[col].median():.2f}'
    axes[i].text(0.05, 0.95, stats_text, transform=axes[i].transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Remove empty subplot
axes[5].set_visible(False)
plt.tight_layout()
plt.show()

# 4. BIVARIATE ANALYSIS
print("\n4. BIVARIATE ANALYSIS")
print("=" * 50)

# Price by different categories
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
axes = axes.ravel()

# Price by Model
top_models = df['Model'].value_counts().head(8).index
model_price_data = df[df['Model'].isin(top_models)]
sns.boxplot(data=model_price_data, x='Model', y='Price_USD', ax=axes[0])
axes[0].set_title('Price Distribution by Model (Top 8)')
axes[0].tick_params(axis='x', rotation=45)

# Price by Region
sns.boxplot(data=df, x='Region', y='Price_USD', ax=axes[1])
axes[1].set_title('Price Distribution by Region')
axes[1].tick_params(axis='x', rotation=45)

# Price by Fuel Type
sns.boxplot(data=df, x='Fuel_Type', y='Price_USD', ax=axes[2])
axes[2].set_title('Price Distribution by Fuel Type')
axes[2].tick_params(axis='x', rotation=45)

# Price by Transmission
sns.boxplot(data=df, x='Transmission', y='Price_USD', ax=axes[3])
axes[3].set_title('Price Distribution by Transmission')

# Price by Sales Classification
sns.boxplot(data=df, x='Sales_Classification', y='Price_USD', ax=axes[4])
axes[4].set_title('Price Distribution by Sales Classification')

# Remove empty subplot
axes[5].set_visible(False)
plt.tight_layout()
plt.show()

# 5. CORRELATION ANALYSIS
print("\n5. CORRELATION ANALYSIS")
print("=" * 50)

# Correlation matrix for numerical variables
correlation_matrix = df[numerical_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
           square=True, linewidths=0.5)
plt.title('Correlation Matrix of Numerical Variables')
plt.tight_layout()
plt.show()

print("Correlation with Price_USD:")
price_correlations = correlation_matrix['Price_USD'].sort_values(ascending=False)
print(price_correlations)

# 6. TIME SERIES ANALYSIS (BY YEAR)
print("\n6. TIME SERIES ANALYSIS")
print("=" * 50)

yearly_stats = df.groupby('Year').agg({
    'Price_USD': ['mean', 'median', 'count'],
    'Mileage_KM': 'mean',
    'Sales_Volume': 'sum'
}).round(2)

yearly_stats.columns = ['Avg_Price', 'Median_Price', 'Count', 'Avg_Mileage', 'Total_Sales']
print("Yearly Statistics:")
print(yearly_stats)

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Average Price trend
axes[0,0].plot(yearly_stats.index, yearly_stats['Avg_Price'], marker='o', linewidth=2)
axes[0,0].set_title('Average Price Trend by Year')
axes[0,0].set_xlabel('Year')
axes[0,0].set_ylabel('Average Price (USD)')
axes[0,0].grid(True, alpha=0.3)

# Sales count by year
axes[0,1].bar(yearly_stats.index, yearly_stats['Count'])
axes[0,1].set_title('Number of Cars by Year')
axes[0,1].set_xlabel('Year')
axes[0,1].set_ylabel('Count')
axes[0,1].tick_params(axis='x', rotation=45)

# Average Mileage by year
axes[1,0].plot(yearly_stats.index, yearly_stats['Avg_Mileage'], marker='s', color='green', linewidth=2)
axes[1,0].set_title('Average Mileage by Year')
axes[1,0].set_xlabel('Year')
axes[1,0].set_ylabel('Average Mileage (KM)')
axes[1,0].grid(True, alpha=0.3)

# Total Sales Volume by year
axes[1,1].bar(yearly_stats.index, yearly_stats['Total_Sales'])
axes[1,1].set_title('Total Sales Volume by Year')
axes[1,1].set_xlabel('Year')
axes[1,1].set_ylabel('Total Sales Volume')
axes[1,1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# 7. MULTIVARIATE ANALYSIS
print("\n7. MULTIVARIATE ANALYSIS")
print("=" * 50)

# Scatter plot matrix
scatter_vars = ['Price_USD', 'Mileage_KM', 'Engine_Size_L', 'Year']
sns.pairplot(df[scatter_vars], diag_kind='hist', corner=True)
plt.suptitle('Scatter Plot Matrix of Key Variables', y=1.02)
plt.show()

# Price vs Mileage colored by Fuel Type
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='Mileage_KM', y='Price_USD', hue='Fuel_Type', alpha=0.6)
plt.title('Price vs Mileage by Fuel Type')
plt.xlabel('Mileage (KM)')
plt.ylabel('Price (USD)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 8. SALES CLASSIFICATION ANALYSIS
print("\n8. SALES CLASSIFICATION ANALYSIS")
print("=" * 50)

classification_summary = df.groupby('Sales_Classification').agg({
    'Price_USD': ['mean', 'median', 'std'],
    'Mileage_KM': ['mean', 'median'],
    'Sales_Volume': ['mean', 'sum'],
    'Model': 'count'
}).round(2)

classification_summary.columns = ['Avg_Price', 'Median_Price', 'Std_Price', 
                                'Avg_Mileage', 'Median_Mileage', 
                                'Avg_Sales_Vol', 'Total_Sales_Vol', 'Count']
print("Sales Classification Summary:")
print(classification_summary)

# Compare High vs Low sales classification
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# Price comparison
sns.boxplot(data=df, x='Sales_Classification', y='Price_USD', ax=axes[0,0])
axes[0,0].set_title('Price by Sales Classification')

# Mileage comparison
sns.boxplot(data=df, x='Sales_Classification', y='Mileage_KM', ax=axes[0,1])
axes[0,1].set_title('Mileage by Sales Classification')

# Engine Size comparison
sns.boxplot(data=df, x='Sales_Classification', y='Engine_Size_L', ax=axes[0,2])
axes[0,2].set_title('Engine Size by Sales Classification')

# Sales Volume comparison
sns.boxplot(data=df, x='Sales_Classification', y='Sales_Volume', ax=axes[1,0])
axes[1,0].set_title('Sales Volume by Sales Classification')

# Year comparison
sns.boxplot(data=df, x='Sales_Classification', y='Year', ax=axes[1,1])
axes[1,1].set_title('Year by Sales Classification')

# Remove empty subplot
axes[1,2].set_visible(False)
plt.tight_layout()
plt.show()

# 9. REGIONAL ANALYSIS
print("\n9. REGIONAL ANALYSIS")
print("=" * 50)

regional_summary = df.groupby('Region').agg({
    'Price_USD': ['mean', 'median', 'count'],
    'Mileage_KM': 'mean',
    'Sales_Volume': 'sum',
    'Year': 'mean'
}).round(2)

regional_summary.columns = ['Avg_Price', 'Median_Price', 'Count', 'Avg_Mileage', 'Total_Sales', 'Avg_Year']
print("Regional Summary:")
print(regional_summary) 

# 10. OUTLIER DETECTION
print("\n10. OUTLIER DETECTION")
print("=" * 50)

# Z-score method for outlier detection
z_scores = stats.zscore(df[numerical_cols])
outliers = (np.abs(z_scores) > 3).sum(axis=0)

print("Number of outliers (Z-score > 3) for each numerical variable:")
for col, outlier_count in zip(numerical_cols, outliers):
    print(f"{col}: {outlier_count} outliers")

# Visualize outliers using boxplots
plt.figure(figsize=(15, 8))
df[numerical_cols].boxplot()
plt.title('Boxplots of Numerical Variables (Outlier Detection)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 11. KEY INSIGHTS SUMMARY
print("\n11. KEY INSIGHTS SUMMARY")
print("=" * 50)

print(f"• Dataset contains {len(df)} BMW vehicle records from {df['Year'].min()} to {df['Year'].max()}")
print(f"• Price range: ${df['Price_USD'].min():,.0f} to ${df['Price_USD'].max():,.0f}")
print(f"• Most common model: {df['Model'].value_counts().index[0]}")
print(f"• Most active region: {df['Region'].value_counts().index[0]}")
print(f"• Most popular fuel type: {df['Fuel_Type'].value_counts().index[0]}")
print(f"• Transmission preference: {df['Transmission'].value_counts().index[0]} ({df['Transmission'].value_counts().iloc[0]} vehicles)")
print(f"• Sales classification: {df['Sales_Classification'].value_counts().to_dict()}")

# Calculate some business metrics
avg_price_high_sales = df[df['Sales_Classification'] == 'High']['Price_USD'].mean()
avg_price_low_sales = df[df['Sales_Classification'] == 'Low']['Price_USD'].mean()

print(f"• Average price - High sales: ${avg_price_high_sales:,.0f}")
print(f"• Average price - Low sales: ${avg_price_low_sales:,.0f}")
print(f"• Price difference: ${(avg_price_high_sales - avg_price_low_sales):,.0f}")

print("\n=== EDA COMPLETE ===")