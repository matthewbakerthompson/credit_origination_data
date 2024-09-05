"""
File:        enhanced_credit_risk_data.py
Author:      Matthew Thompson - matthewbakerthompson@gmail.com
Date:        9.4.24
Description:
    This script generates a synthetic dataset of customer credit information for use in 
    credit risk modeling. The dataset includes various customer attributes such as age, 
    income, education level, employment status, and credit-related variables such as credit 
    score, debt-to-income (DTI) ratio, and payment history. Additionally, it calculates 
    various metrics like credit score category and debt type breakdown.

Features:
    - Generates synthetic data with common customer and credit attributes (e.g., age, income, debt).
    - Adjusts credit score based on factors like education, income, debt-to-income ratio, and payment history.
    - Includes a weighted calculation of various debt types such as credit card debt, mortgage debt, and auto loan debt.
    - Simulates payment history and impacts of delinquency and bankruptcy.
    - Outputs the dataset into a CSV file and prints a preview along with credit score distribution.

Inputs:
    - None (All data is generated synthetically using the Faker library and NumPy)

Outputs:
    - enhanced_credit_risk_data.csv: The generated dataset containing customer credit information.
    - Credit score distribution printed to the console.

Usage:
    python enhanced_credit_risk_data.py

Dependencies:
    - pandas
    - faker
    - numpy
"""


import pandas as pd
from faker import Faker
import numpy as np
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Define the number of samples
num_samples = 10000

# Age distribution parameters
mean_age = 40
std_dev_age = 12

# Income distribution parameters
mean_income = 75000
std_dev_income = 30000

# Define regions to simmulate income distributions
regions = ['Northeast', 'Midwest', 'South', 'West']
income_adjustment = {'Northeast': 1.1, 'Midwest': 0.9, 'South': 0.8, 'West': 1.0}
regional_cost_of_living = {'Northeast': 1.2, 'Midwest': 0.8, 'South': 0.9, 'West': 1.1}

# Define education and income multipliers to simulate education impact
education_income_multiplier = {
    'Less than High School': 0.6,
    'High School': 0.8,
    'Associate\'s Degree': 1.0,
    'Bachelor\'s Degree': 1.2,
    'Master\'s Degree': 1.4,
    'Doctorate': 1.6
}

# Define employment status impact on income
employment_income_multiplier = {
    'Full-Time': 1.0,
    'Part-Time': 0.6,
    'Self-Employed': 0.9,
    'Unemployed': 0.2,
    'Retired': 0.7
}

# Generate the sample data
data = {
    'Customer_ID': [fake.uuid4() for _ in range(num_samples)],
    'Name': [fake.name() for _ in range(num_samples)],
    'Age': np.random.normal(mean_age, std_dev_age, num_samples).astype(int),
    'Gender': np.random.choice(['Male', 'Female'], num_samples),
    'Region': np.random.choice(regions, size=num_samples),
    'Education_Level': np.random.choice(['Less than High School', 'High School', 'Associate\'s Degree', 'Bachelor\'s Degree', 'Master\'s Degree', 'Doctorate'], num_samples),
    'Employment_Status': np.random.choice(['Full-Time', 'Part-Time', 'Self-Employed', 'Unemployed', 'Retired'], num_samples),
    'Income': np.zeros(num_samples).astype(int),  # Placeholder for adjusted income
    'Credit_Score': np.zeros(num_samples),  # Placeholder
    'Existing_Debt': np.zeros(num_samples).astype(float),  # Placeholder
    'Credit_Card_Debt': np.zeros(num_samples).astype(float),  # New debt type
    'Mortgage_Debt': np.zeros(num_samples).astype(float),  # New debt type
    'Auto_Loan_Debt': np.zeros(num_samples).astype(float),  # New debt type
    'Loan_Balance': np.random.normal(10000, 5000, num_samples).astype(float),
    'Credit_Inquiries_Last_6_Months': np.random.randint(0, 10, num_samples),
    'Bankruptcy_History': np.random.choice(['Yes', 'No'], num_samples, p=[0.1, 0.9]),
    'Bankruptcy_Date': [None] * num_samples,  # Placeholder for Bankruptcy Date
    'Delinquency_History': np.random.randint(0, 5, num_samples),
    'Credit_Card_Utilization': np.random.uniform(0.0, 1.0, num_samples).round(2),
    'Years_At_Current_Address': np.random.randint(0, 30, num_samples),
    'Dependents': np.random.randint(0, 4, num_samples),  
    'Payment_History': np.zeros(num_samples, dtype=str),  # Placeholder
    'Account_Age': np.zeros(num_samples).astype(int),  # Placeholder
    'Years_With_Employer': np.zeros(num_samples).astype(int),  # Placeholder
    'Housing': np.random.choice(['Rent', 'Own'], num_samples),
    'Housing_Payment': np.zeros(num_samples).astype(float)  # Placeholder
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Adjust income based on education, employment, and region
df['Income'] = df.apply(lambda row: np.random.normal(mean_income, std_dev_income) * 
                        income_adjustment[row['Region']] * 
                        education_income_multiplier[row['Education_Level']] * 
                        employment_income_multiplier[row['Employment_Status']], axis=1)

# Adjust the maximum income to 500,000 do to lower end credit consumer target
df['Income'] = df['Income'].clip(20000, 500000)

# Generate years with the current employer based on age with an adjusted realistic distribution
def generate_years_with_employer(age):
    if age < 30:
        return np.random.randint(0, 5)  # Shorter tenures for younger individuals
    elif 30 <= age < 50:
        return np.random.randint(0, 15)  # Mid-range tenures
    else:
        return np.random.choice([np.random.randint(0, 15), np.random.randint(15, 30)], p=[0.8, 0.2])  # Longer tenures more likely for older individuals

df['Years_With_Employer'] = df['Age'].apply(generate_years_with_employer)

# Generate a bankruptcy date if the customer has a bankruptcy history
def generate_bankruptcy_date(bankruptcy_history):
    if bankruptcy_history == 'Yes':
        # Generate a random date within the last 20 years
        days_ago = np.random.randint(0, 365*20)  # Up to 20 years ago
        return datetime.now() - timedelta(days=days_ago)
    else:
        return None

df['Bankruptcy_Date'] = df['Bankruptcy_History'].apply(generate_bankruptcy_date)

# Base Credit Score Distribution (reflects real population distribution)
score_distribution = {
    '300-579': 0.16,
    '580-669': 0.18,
    '670-739': 0.21,
    '740-799': 0.25,
    '800-850': 0.20
}

# Sample from this distribution
df['Credit_Score'] = np.random.choice(
    [np.random.uniform(300, 579), np.random.uniform(580, 669), np.random.uniform(670, 739), 
     np.random.uniform(740, 799), np.random.uniform(800, 850)],
    size=num_samples, p=[0.16, 0.18, 0.21, 0.25, 0.20]
)

# Adjust Credit Score based on Income, Employment Status, and Debt-to-Income Ratio (DTI)
df['Existing_Debt'] = df['Income'] * np.random.uniform(0.1, 0.5, num_samples)  # Existing debt as a percentage of income
df['DTI'] = df['Existing_Debt'] / df['Income']  # Calculate Debt-to-Income Ratio

# Adjust credit score with milder reductions based on DTI
df['Credit_Score'] = df.apply(lambda row: row['Credit_Score'] - (row['DTI'] * 50), axis=1)

# Adjust credit score based on how recent the bankruptcy was
def adjust_credit_score_by_bankruptcy(credit_score, bankruptcy_date):
    if bankruptcy_date is not None:
        years_since_bankruptcy = (datetime.now() - bankruptcy_date).days / 365
        if years_since_bankruptcy < 7:
            return credit_score - 50  # Milder impact
        elif 7 <= years_since_bankruptcy < 10:
            return credit_score - 20  # Moderate impact
        else:
            return credit_score - 5  # Minimal impact
    else:
        return credit_score

df['Credit_Score'] = df.apply(lambda row: adjust_credit_score_by_bankruptcy(row['Credit_Score'], row['Bankruptcy_Date']), axis=1)

# Generate specific types of debt
df['Credit_Card_Debt'] = df['Income'] * np.random.uniform(0.05, 0.2, num_samples)
df['Mortgage_Debt'] = df.apply(lambda row: row['Income'] * np.random.uniform(1.0, 3.0) if row['Housing'] == 'Own' else 0, axis=1)
df['Auto_Loan_Debt'] = df['Income'] * np.random.uniform(0.1, 0.5, num_samples)

# Update DTI with the new debts included
df['Total_Debt'] = df['Existing_Debt'] + df['Credit_Card_Debt'] + df['Mortgage_Debt'] + df['Auto_Loan_Debt']
df['DTI'] = df['Total_Debt'] / df['Income']

# Simulate payment history with a more balanced distribution
def simulate_payment_history(credit_score, delinquency_history, bankruptcy_history):
    if bankruptcy_history == 'Yes':
        return 'Poor'
    elif delinquency_history > 3:
        return 'Poor'
    else:
        if credit_score >= 750:
            return np.random.choice(['Excellent', 'Good'], p=[0.7, 0.3])
        elif 650 <= credit_score < 750:
            return np.random.choice(['Good', 'Average'], p=[0.4, 0.6])
        else:
            return np.random.choice(['Average', 'Poor'], p=[0.3, 0.7])

df['Payment_History'] = df.apply(lambda row: simulate_payment_history(row['Credit_Score'], row['Delinquency_History'], row['Bankruptcy_History']), axis=1)

# Generate account age based on the customer's age with a cap at age - 18
def generate_account_age(age):
    if age > 18:
        return np.random.randint(0, min(age - 18, age))
    else:
        return 0  # Default or minimum account age

df['Account_Age'] = df['Age'].apply(generate_account_age)

# Calculate credit history length, ensuring it doesn't exceed age - 18
df['Credit_History_Length'] = df.apply(lambda row: max(0, row['Age'] - 18 - row['Account_Age']), axis=1)

# Adjust credit score based on credit history length
df['Credit_Score'] = df.apply(lambda row: row['Credit_Score'] + (row['Credit_History_Length'] * 0.5), axis=1)

# Adjust credit score based on credit utilization rate
def adjust_credit_score_by_utilization(credit_score, utilization):
    if utilization > 0.75:
        return credit_score - 25  # Lighter impact if utilization is high
    elif utilization > 0.5:
        return credit_score - 10  # Lighter moderate impact
    else:
        return credit_score

df['Credit_Score'] = df.apply(lambda row: adjust_credit_score_by_utilization(row['Credit_Score'], row['Credit_Card_Utilization']), axis=1)

# Introduce outliers in Income and Debt
outliers_idx = np.random.choice(df.index, size=int(0.01 * len(df)), replace=False)
df.loc[outliers_idx, 'Income'] *= np.random.choice([2, 3], size=len(outliers_idx))
df.loc[outliers_idx, 'Total_Debt'] *= np.random.choice([1.5, 2], size=len(outliers_idx))

# Generate housing payment based on whether the customer rents or owns, with regional adjustment
def generate_housing_payment(housing, income, region, dependents):
    if housing == 'Rent':
        return np.random.randint(500, 3500) * regional_cost_of_living[region] * (1 + dependents * 0.1)  # Adjusted rent payments range by region and dependents
    else:
        return np.random.randint(900, 4500) * regional_cost_of_living[region] * (1 + dependents * 0.1)  # Adjusted mortgage payments range by region and dependents

df['Housing_Payment'] = df.apply(lambda row: generate_housing_payment(row['Housing'], row['Income'], row['Region'], row['Dependents']), axis=1)

# Final adjustments and clipping to realistic values
df['Age'] = df['Age'].clip(18, 70)
df['Income'] = df['Income'].clip(20000, 400000)
df['Credit_Score'] = df['Credit_Score'].clip(300, 850)
df['Existing_Debt'] = df['Existing_Debt'].clip(0, df['Income'] * 0.5)

# Add a new column displaying the credit score category based on bins
score_bins = [300, 580, 670, 740, 800, 850]
score_labels = ['Very Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
df['Credit_Score_Category'] = pd.cut(df['Credit_Score'], bins=score_bins, labels=score_labels, include_lowest=True)

# Save to a CSV file, keeping number format
df.to_csv('enhanced_credit_risk_data.csv', index=False, float_format='%.2f')

# Display distribution of credit scores
print("\nCredit Score Distribution:")
print(df['Credit_Score_Category'].value_counts(normalize=True).sort_index())

# Display the first few rows
print(df.head())