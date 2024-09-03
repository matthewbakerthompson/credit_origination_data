# Enhanced Credit Risk Dataset Generation

This Python script is designed to generate a realistic synthetic dataset that simulates the financial profiles of individuals, focusing on factors relevant to credit risk assessment. The dataset includes a variety of attributes that contribute to a comprehensive view of each individual's creditworthiness. The script utilizes the `Faker` library to generate personal information and realistic data distributions for financial variables, while also incorporating logic that reflects real-world credit risk modeling practices.

## Key Features and Variables

### 1. Personal Information:
- **Customer_ID**: A unique identifier for each individual.
- **Name**: A randomly generated name for each individual.
- **Age**: The age of the individual, normally distributed with a mean of 40 years and a standard deviation of 12 years.
- **Gender**: The gender of the individual, randomly chosen as either 'Male' or 'Female'.
- **Region**: The region in which the individual resides, with options including 'Northeast,' 'Midwest,' 'South,' and 'West'.

### 2. Socioeconomic and Employment Variables:
- **Education_Level**: The highest education level attained by the individual, which influences income and credit score. Options range from 'Less than High School' to 'Doctorate.'
- **Employment_Status**: The current employment status of the individual, affecting their income. Options include 'Full-Time,' 'Part-Time,' 'Self-Employed,' 'Unemployed,' and 'Retired.'
- **Years_With_Employer**: The number of years the individual has been with their current employer, with realistic distributions based on age.

### 3. Financial Variables:
- **Income**: The individual's annual income, adjusted by education level, employment status, and region. Income is capped at a maximum of $400,000.
- **Existing_Debt**: The total existing debt of the individual, calculated as a percentage of their income.
- **Credit_Card_Debt**: Specific debt related to credit card balances.
- **Mortgage_Debt**: Debt related to home ownership, applicable only if the individual owns a home.
- **Auto_Loan_Debt**: Debt related to vehicle loans.
- **Total_Debt**: The sum of all debt types, used to calculate the Debt-to-Income Ratio (DTI).
- **Credit_Score**: A critical variable representing the individual's credit score, which is influenced by income, education level, DTI, credit utilization, and other factors. The score is carefully clipped to remain within the standard range of 300 to 850.

### 4. Credit Behavior and History:
- **Credit_Inquiries_Last_6_Months**: The number of credit inquiries made in the last six months, which can impact the credit score.
- **Bankruptcy_History**: A binary indicator showing whether the individual has a history of bankruptcy.
- **Delinquency_History**: The number of past delinquencies, influencing the credit score and payment history.
- **Credit_Card_Utilization**: The ratio of current credit card balances to credit limits, affecting the credit score.
- **Credit_History_Length**: The length of the individual's credit history, calculated as the difference between their age and the age at which they first received credit (capped at age - 18).

### 5. Housing and Stability:
- **Housing**: Indicates whether the individual rents or owns their home.
- **Years_At_Current_Address**: The number of years the individual has lived at their current address, with distributions reflecting typical residential stability based on age.
- **Housing_Payment**: The monthly payment for housing, adjusted by region and the number of dependents.

### 6. Additional Factors:
- **Dependents**: The number of dependents the individual supports, which can influence housing payments and overall financial stress.
- **Payment_History**: A classification of the individual's payment history into categories such as 'Excellent,' 'Good,' 'Average,' and 'Poor,' based on factors like credit score, delinquency history, and bankruptcy status.

## Distribution and Logic
- **Income and Debt**: Income is generated with regional and educational adjustments, and debt levels are calculated as a function of income. Specific types of debt (e.g., mortgage, auto loans) are also calculated, contributing to the individual's total debt load.
- **Credit Score Adjustments**: The credit score is influenced by a variety of factors, including Debt-to-Income Ratio (DTI), credit card utilization, payment history, and credit history length. The score is clipped to remain within the realistic range of 300 to 850.
- **Housing and Stability**: Housing payments are adjusted based on whether the individual rents or owns, as well as the regional cost of living and the number of dependents. Years at the current address are distributed to reflect typical residential stability, with younger individuals having shorter stays, while older individuals potentially having longer stays.
- **Outliers**: Outliers are introduced in income and debt to reflect the financial diversity found in real-world populations.

## Output
- The dataset is generated and saved as a CSV file named `enhanced_credit_risk_data.csv`. This file contains the complete set of variables described above, providing a rich dataset for modeling and analysis.

---

This script provides a realistic and comprehensive dataset for testing and developing credit risk models, taking into account various factors that impact an individual's creditworthiness. The generated data is ideal for machine learning, statistical analysis, or any other credit risk assessment tasks.
