import pandas as pd

# Load dataset
df = pd.read_csv("data/Hospital ER_Data.csv")

# Show first rows
print(df.head())

# Dataset info
print("\nDataset Info:")
df.info()

# Average wait time
avg_wait = df["Patient Waittime"].mean()
print("\nAverage Wait Time:", avg_wait)

# Patients per department
dept_counts = df["Department Referral"].value_counts()
print("\nPatients per Department:")
print(dept_counts)

# Admission statistics
admission_counts = df["Patient Admission Flag"].value_counts()
print("\nAdmission vs Discharge:")
print(admission_counts)