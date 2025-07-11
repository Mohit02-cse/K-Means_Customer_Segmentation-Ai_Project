
# Importing Required Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load Dataset
file_path = "/content/Customers.csv"
df = pd.read_csv(file_path)

# Display Dataset Overview
print("Dataset Shape:", df.shape)
print("First 5 Rows:\n", df.head())
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())

# Exploratory Data Analysis (EDA)

# Summary statistics
print("\nSummary Statistics:\n", df.describe(),"\n\n")


# Distribution plots
plt.figure(figsize=(12,5))
plt.subplot(1, 2, 1)
sns.histplot(df['Age'], kde=True)
plt.title('Age Distribution')

plt.subplot(1, 2, 2)
sns.histplot(df['Annual Income ($)'], kde=True)
plt.title('Annual Income Distribution')
plt.show()
print("\n\n")

# Correlation Heatmap
plt.figure(figsize=(8, 5))
# Calculate correlation only for numeric columns
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlation Heatmap")
plt.show()
print("\n\n")

# Feature Selection
X = df[['Age', 'Annual Income ($)']].values

# Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Determine Optimal Number of Clusters using Elbow Method
wcss = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# Plotting the Elbow Curve
plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), wcss, 'bo-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('WCSS')
plt.title('Elbow Method for Optimal k')
plt.grid()
plt.show()
print("\n\n")

# From the Elbow, suppose optimal k = 3
optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
kmeans.fit(X_scaled)

# Cluster Centers (unscaled)
centers = scaler.inverse_transform(kmeans.cluster_centers_)

# Assign cluster labels to data
labels = kmeans.labels_
df['Cluster'] = labels

# Visualizing the Clusters
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Age', y='Annual Income ($)', hue='Cluster', data=df, palette='viridis')
plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='X', s=200, label='Centroids')
plt.title('Customer Segmentation (K-Means Clustering)')
plt.xlabel('Age')
plt.ylabel('Annual Income ($)')
plt.legend()
plt.grid(True)
plt.show()
print("\n\n")

# Display Cluster Centers
print("Cluster Centers (Age, Annual Income):\n", centers)

# Quick Summary of Clusters
cluster_summary = df.groupby('Cluster').agg({
    'Age': ['mean', 'min', 'max'],
    'Annual Income ($)': ['mean', 'min', 'max'],
    'Cluster': 'count'
}).rename(columns={'Cluster': 'Customer Count'})

print("\nCluster Summary:\n", cluster_summary)
