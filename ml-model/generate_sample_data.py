"""
Generate sample employee attrition dataset for training
"""
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Number of samples
n_samples = 5000

# Generate synthetic data
data = {
    'employee_id': range(1, n_samples + 1),
    'salary_growth': np.random.uniform(-5, 25, n_samples),  # -5% to 25% annual growth
    'performance_score': np.random.uniform(1, 5, n_samples),  # 1-5 scale
    'promotion_gap': np.random.randint(0, 10, n_samples),  # years since last promotion
    'satisfaction_score': np.random.uniform(1, 10, n_samples),  # 1-10 scale
    'work_hours': np.random.uniform(35, 70, n_samples),  # weekly hours
    'overtime_frequency': np.random.uniform(0, 40, n_samples),  # hours per month
}

# Create DataFrame
df = pd.DataFrame(data)

# Generate attrition based on realistic patterns
# Higher attrition probability when:
# - Low salary growth
# - Low performance score
# - Long promotion gap
# - Low satisfaction
# - High work hours
# - High overtime

attrition_probability = (
    (1 - (df['salary_growth'] + 5) / 30) * 0.2 +  # Low salary growth increases risk
    (1 - df['performance_score'] / 5) * 0.15 +  # Low performance increases risk
    (df['promotion_gap'] / 10) * 0.25 +  # Long promotion gap increases risk
    (1 - df['satisfaction_score'] / 10) * 0.25 +  # Low satisfaction increases risk
    ((df['work_hours'] - 35) / 35) * 0.1 +  # High work hours increase risk
    (df['overtime_frequency'] / 40) * 0.05  # High overtime increases risk
)

# Add some randomness
attrition_probability = np.clip(attrition_probability + np.random.normal(0, 0.1, n_samples), 0, 1)

# Generate binary attrition labels
df['attrition'] = (attrition_probability > 0.5).astype(int)

# Add some noise to make it more realistic
noise_indices = np.random.choice(n_samples, size=int(n_samples * 0.1), replace=False)
df.loc[noise_indices, 'attrition'] = 1 - df.loc[noise_indices, 'attrition']

# Save to CSV
df.to_csv('ml-model/employee_data.csv', index=False)

print(f"Generated {n_samples} employee records")
print(f"Attrition rate: {df['attrition'].mean():.2%}")
print(f"\nDataset saved to: ml-model/employee_data.csv")
print(f"\nDataset shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nAttrition distribution:")
print(df['attrition'].value_counts())
print(f"\nFeature statistics:")
print(df.describe())
