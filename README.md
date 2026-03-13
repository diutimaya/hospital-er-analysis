# Hospital Emergency Room Analytics

## Dashboard Preview

![Hospital ER Dashboard](dashboard/hospital_er_dashboard.png)

---

## Project Overview

This project analyzes hospital emergency room (ER) data to understand **patient flow, waiting times, department workload, and patient satisfaction trends**.

The goal is to extract insights that can help hospitals improve **resource allocation, reduce waiting times, and enhance operational efficiency**.

The analysis includes **data cleaning, exploratory data analysis using Python, and interactive data visualization using Tableau**.

---

## Dataset

The dataset contains **9,216 emergency room patient records** with the following attributes:

* Patient ID
* Patient Admission Date
* Patient Gender
* Patient Age
* Patient Race
* Department Referral
* Patient Admission Flag
* Patient Satisfaction Score
* Patient Waittime

---

## Technologies Used

* **Python**
* **Pandas**
* **NumPy**
* **Matplotlib**
* **Seaborn**
* **Jupyter Notebook**
* **Tableau Public**
* **Git & GitHub**

---

## Project Structure

```
hospital-er-analysis
│
├── data
│   └── Hospital ER Data.csv
│
├── notebook
│   └── er_analysis.ipynb
│
├── src
│   └── analysis.py
│
├── dashboard
│   └── hospital_er_dashboard.png
│
├── requirements.txt
│
└── README.md
```

---

## Data Cleaning

The following preprocessing steps were performed:

* Removed unnecessary columns such as patient initials and last names
* Handled missing values in **Department Referral**
* Filled missing **Patient Satisfaction Scores** with the average value
* Converted **Patient Admission Date** to datetime format for time-based analysis

---

## Exploratory Data Analysis

Several analyses were performed to understand ER behavior:

## Department Workload

Analyzed the number of patients referred to each department to identify **high-demand services**.

## Wait Time Distribution

Examined how long patients typically wait before receiving treatment.

## Wait Time vs Patient Satisfaction

Analyzed whether longer waiting times influence patient satisfaction levels.

## Patient Arrival by Hour

Extracted admission hour to identify **peak hospital hours**.

## Age Distribution

Studied the distribution of patient ages visiting the emergency room.

## Age Group Segmentation

Grouped patients into the following categories:

* Child
* Young Adult
* Adult
* Middle Age
* Senior

---

## Key Insights

* **General Practice** receives the highest number of patient referrals.
* The average emergency room wait time is approximately **35 minutes**.
* Most patients belong to the **Adult and Middle Age groups**.
* Patient satisfaction tends to **decrease slightly as wait time increases**.
* Emergency room visits occur **consistently throughout the day**, with slight increases during evening hours.

---

## Dashboard

The Tableau dashboard provides visual insights into:

* Department workload
* Waiting time patterns
* Patient satisfaction trends
* Patient arrival patterns
* Age distribution of ER patients

The dashboard combines multiple visualizations to give a **comprehensive overview of emergency room operations**.

---

## How to Run the Project

Clone the repository:

```
git clone https://github.com/diutimaya/hospital-er-analysis.git
```

Navigate to the project directory:

```
cd hospital-er-analysis
```

Install required libraries:

```
pip install -r requirements.txt
```

Run the analysis script:

```
python src/analysis.py
```

---

## Future Improvements

Possible extensions of this project include:

* Building a **Power BI or web-based dashboard**
* Applying **machine learning models to predict ER wait time**
* Predicting **patient admission probability**
* Analyzing **seasonal hospital traffic patterns**
* Deploying the dashboard as an **interactive analytics application**

---

## Author

**Diutimaya Mohanty**
B.Tech Student — Data Science Specialization
