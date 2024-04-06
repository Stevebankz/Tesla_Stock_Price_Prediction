# -*- coding: utf-8 -*-
"""Tesla-Stock-Priceipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mnt73q3YXDFHRvHUXiKtEFiAoD3-w0Kg
"""

# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # Renamed seaborn to sns for brevity

# Import machine learning modules
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn import metrics

import warnings
warnings.filterwarnings('ignore')  # Suppress warnings during execution

# Reading the CSV file 'TSLA.csv' into a pandas DataFrame
# Assumption: 'TSLA.csv' file is located in the current directory
df = pd.read_csv('TSLA.csv')

# Displaying the first few rows of the DataFrame to inspect the data
df.head()

# Displaying the shape of the DataFrame (number of rows, number of columns)
df.shape

# Generating descriptive statistics of the DataFrame
df.describe()

# Displaying concise summary information about the DataFrame, including column data types and non-null counts
df.info()

# Setting the size of the plot figure
plt.figure(figsize=(10, 6))

# Plotting the 'Close' column from the DataFrame with a unique color and linestyle
plt.plot(df['Close'], color='magenta', linestyle='--', linewidth=2)

# Adding title to the plot with a unique font style
plt.title('Tesla Closing Price Trend', fontsize=18, fontweight='bold', color='navy')

# Adding label to the y-axis with a unique font style
plt.ylabel('Closing Price (USD)', fontsize=14, fontweight='bold', color='darkgreen')

# Adding label to the x-axis with a unique font style
plt.xlabel('Date', fontsize=14, fontweight='bold', color='darkgreen')

# Customizing the gridlines with a unique color
plt.grid(color='lightgrey', linestyle='--', linewidth=0.5)

# Adding a background color to the plot
plt.gca().set_facecolor('whitesmoke')

# Adding horizontal line at average closing price for reference
average_price = df['Close'].mean()
plt.axhline(average_price, color='gray', linestyle='-', linewidth=1.5, label='Average Price')

# Adding a legend to the plot
plt.legend(loc='upper left', fontsize=12)

# Displaying the plot
plt.show()

# Displaying the first few rows of the DataFrame
df.head()

# Filtering rows where the 'Close' column is equal to the 'Adj Close' column,
# and displaying the shape of the resulting DataFrame
df[df['Close'] == df['Adj Close']].shape

# Dropping the 'Adj Close' column from the DataFrame along the column axis
df = df.drop(['Adj Close'], axis=1)

# Calculating the sum of missing values in each column of the DataFrame
df.isnull().sum()

# New color palette
custom_palette = ['#FF5733', '#33FF57', '#3357FF', '#FFFF33', '#33FFFF']

# New figure size
plt.figure(figsize=(15, 8))

features = ['Open', 'High', 'Low', 'Close', 'Volume']

for i, col in enumerate(features):
    plt.subplot(2, 3, i + 1)
    sns.histplot(df[col], color=custom_palette[i], kde=True)
    plt.title(f'Distribution of {col}', fontsize=14, color='navy', fontweight='bold')
    plt.xlabel('Values', fontsize=12, color='maroon')
    plt.ylabel('Frequency', fontsize=12, color='maroon')
    plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# Splitting the 'Date' column into separate columns for day, month, and year
splitted = df['Date'].str.split('-', expand=True)

# Adding a new column 'day' with the day component of the date
df['day'] = splitted[2].astype('int')

# Adding a new column 'month' with the month component of the date
df['month'] = splitted[1].astype('int')

# Adding a new column 'year' with the year component of the date
df['year'] = splitted[0].astype('int')

# Displaying the modified DataFrame with new columns
df.head()

# Adding a new column 'is_quarter_end' indicating whether the month is the end of a quarter
df['is_quarter_end'] = np.where(df['month'] % 3 == 0, 1, 0)

# Displaying the DataFrame with the new 'is_quarter_end' column
df.head()

df['open-close'] = df['Open'] - df['Close']
df['low-high'] = df['Low'] - df['High']
df['target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)

# Data
target_counts = df['target'].value_counts().values

# Customizing colors
colors = ['#ff9999', '#66b3ff']

# Customizing explode
explode = (0.1, 0)  # Explode the first slice

# Customizing shadow and start angle
plt.pie(target_counts,
        labels=[0, 1],
        autopct='%1.1f%%',
        colors=colors,
        explode=explode,
        shadow=True,
        startangle=140)

# Adding a title
plt.title('Distribution of Target Values')

# Displaying the pie chart
plt.show()

# Selecting features and target variables
features = df[['open-close', 'low-high', 'is_quarter_end']]
target = df['target']

# Scaling the features using StandardScaler
scaler = StandardScaler()
features = scaler.fit_transform(features)

# Splitting the dataset into training and validation sets
X_train, X_valid, Y_train, Y_valid = train_test_split(
    features, target, test_size=0.1, random_state=2022)

# Printing the shapes of the training and validation sets
print(X_train.shape, X_valid.shape)

from sklearn.linear_model import LogisticRegression  # Importing Logistic Regression classifier
from sklearn.svm import SVC  # Importing Support Vector Classifier
from xgboost import XGBClassifier  # Importing XGBoost Classifier
from sklearn import metrics  # Importing metrics for evaluation

# Defining the list of models
models = [LogisticRegression(), SVC(kernel='poly', probability=True), XGBClassifier()]

# Training the models and evaluating performance
for model in models:
    model.fit(X_train, Y_train)
    print(f'{model} : ')
    print('Training Accuracy : ', metrics.roc_auc_score(Y_train, model.predict_proba(X_train)[:,1]))
    print('Validation Accuracy : ', metrics.roc_auc_score(Y_valid, model.predict_proba(X_valid)[:,1]))