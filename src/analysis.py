import pandas as pd

# Load dataset
df = pd.read_csv(r"C:\Users\HP\Downloads\Hospital-er-analysis\data\Hospital ER_Data.csv")

# Show first rows
print(df.head())

# Dataset info
print("\nDataset Info:")
print(df.info())

# Average wait time
avg_wait = df["Patient Waittime"].mean()
print("\nAverage Wait Time:", avg_wait)

# Patients per department
dept_counts = df["Department Referral"].value_counts()
print("\nPatients per Department:")
print(dept_counts)