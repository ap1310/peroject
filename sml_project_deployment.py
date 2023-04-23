# -*- coding: utf-8 -*-
"""Sml project deployment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZDWr0ZpJ2Qa2fzIvLBL1RAko4T7XJCKL

### Importing Necassary Libraries
"""

import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

books=pd.read_csv("books.csv")
books.head()

df=pd.read_csv('issue renew.csv')
df.head()

"""### Data Pre-Processing"""

df.shape

df.info()

df.describe()

df.isnull().sum()

duplicate_titles = df['Title'].value_counts()
duplicate_titles = duplicate_titles[duplicate_titles > 1].reset_index()
duplicate_titles.columns = ['Title', 'Count']

duplicate_titles

df.drop(['Collection', 'Barcode', 'itype', 'Library'], axis=1,inplace=True)
df.head(2)

merged_df = pd.merge(df, duplicate_titles, on='Title', how='left')
merged_df.head()

merged_df.dropna()

merged_df.isna().sum()

def convert_to_rating(Count):
    if Count >50:
        return 5
    elif Count >30:
        return 4
    elif Count > 10:
        return 3
    elif Count > 3:
        return 2
    else:
        return 1

# Add a new column to the dataset with the book ratings
merged_df['Rating'] = merged_df['Count'].apply(convert_to_rating)

"""### Merging the dept column from books to issue data"""

dept= dict(zip(books['Title'], books['Dept.']))
dept

merged_df['Department'] = df.loc[:, 'Title']
merged_df.head()

merged_df['Department'] = merged_df['Department'].map(dept)
merged_df.head()

merged_df.Department.unique()

merged_df.loc[merged_df['Department'] == 'Other']

"""### Merging the dept pages from books to issue data"""

books['Pgs.'].isna().sum()

books['Pgs.'].fillna(100)

books.dtypes

books.head(2)

for i, row in books.iterrows():
    try:
        books.at[i, 'Pgs.'] = int(row['Pgs.'])
    except ValueError:
        books.at[i, 'Pgs.'] = 0

books.dtypes

books['Pgs.'] = books['Pgs.'].astype(int)

books.dtypes

books['Pgs.'].dtypes

pages= dict(zip(books['Title'], books['Pgs.']))
pages

merged_df['Pages'] = df.loc[:, 'Title']
merged_df

merged_df['Pages'] = merged_df['Pages'].map(pages)
merged_df

"""### EDA"""

fig, ax = plt.subplots(figsize=[15,10])
sns.distplot(merged_df['Rating'],ax=ax)
ax.set_title('rating distribution for all books',fontsize=20)
ax.set_xlabel('rating',fontsize=13)

ax = sns.relplot(data=merged_df, x="Rating", y="Count", color = 'red', sizes=(100, 200), height=7, marker='o')
plt.title("Relation between Book Counts and Ratings",fontsize = 15)
ax.set_axis_labels("Rating", "Book Count")

from wordcloud import WordCloud, STOPWORDS

text = " ".join(merged_df['Title'].tolist())

# create a WordCloud object
wordcloud = WordCloud().generate(text)

# plot the wordcloud
plt.figure(figsize=(8,8), facecolor='white')
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

merged_df

merged_df['IssueDate'] = pd.to_datetime(merged_df['IssueDate'], format='%Y-%m-%d %H:%M:%S').dt.month

merged_df

merged_df['IssueDate'].unique()

merged_df['Count'].isnull().sum()

merged_df.dropna(inplace= True)

merged_df

df_filtered = merged_df[~merged_df['Pages'].isin([0.0])]
df_filtered

value=0

zeropages = merged_df[merged_df['Pages'] == value]

zeropages

#as we don't have enough data for pages, we won't be taking it as a factor

merged_df.drop('Pages', axis=1, inplace=True)

merged_df

"""### Label Encoding Features"""

merged_df

merged_df['Title'].nunique()

new_df= merged_df

new_df

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

new_df['Department'] = le.fit_transform(new_df['Department'])

new_df['type'] = le.fit_transform(new_df['type'])

new_df['Author'] = le.fit_transform(new_df['Author'])

new_df['Title'] = le.fit_transform(new_df['Author'])

new_df.dtypes

new_df

new_df['Count'] = new_df['Count'].astype(int)

new_df

new_df["Rating"].unique()

from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd


# select the relevant features and target variable
X = new_df[["Count", "IssueDate", "Department", "type"]]
y = new_df["Rating"]

# split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# create a Ridge regression model with L2 regularization
model = Ridge(alpha=1.0)

# fit the model to the training data
model.fit(X_train, y_train)

# make predictions on the testing data
y_pred = model.predict(X_test)

# compute the mean squared error
mse = mean_squared_error(y_test, y_pred)

print("Mean Squared Error:", mse)

"""### Decision tree  """

from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd

# select the relevant features and target variable
X = new_df[["Count", "IssueDate", "Department", "type"]]
y = new_df["Rating"]

# split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# create a Decision Tree Regressor model
model = DecisionTreeRegressor(max_depth=10)

# use cross-validation to evaluate the model's performance
scores = cross_val_score(model, X, y, cv=5, scoring="neg_mean_squared_error")

# fit the model to the training data
model.fit(X_train, y_train)

# make predictions on the testing data
y_pred = model.predict(X_test)

# compute the mean squared error
mse = mean_squared_error(y_test, y_pred)

print("Cross-validation Mean Squared Error:", -scores.mean())
print("Testing Mean Squared Error:", mse)

from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd

# select the relevant features and target variable
X = new_df[["Count", "IssueDate", "Department", "type"]]
y = new_df["Rating"]

# split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# create a Decision Tree Regressor model
tree = DecisionTreeRegressor(random_state=42)

# define the hyperparameter grid
param_grid = {'max_depth': [5, 10, 15, 20]}

# create a GridSearchCV object with 5-fold cross-validation
grid = GridSearchCV(estimator=tree, param_grid=param_grid, cv=5, scoring="neg_mean_squared_error")

# fit the grid search object to the training data
grid.fit(X_train, y_train)

# get the best estimator and print the best parameters
best_estimator = grid.best_estimator_
print("Best Parameters:", grid.best_params_)

# create a Ridge Regression model with L2 regularization
ridge = Ridge(alpha=0.1)


# fit the Ridge Regression model to the training data
ridge.fit(X_train, y_train)

# make predictions on the testing data using the best estimator and the Ridge Regression model
y_pred1 = best_estimator.predict(X_test)
y_pred2 = ridge.predict(X_test)

# compute the mean squared error for both models
mse1 = mean_squared_error(y_test, y_pred1)
mse2 = mean_squared_error(y_test, y_pred2)

print("Decision Tree Mean Squared Error:", mse1)
print("Ridge Regression Mean Squared Error:", mse2)

"""### Ridge regression"""

from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV

X = new_df[["Count","IssueDate","Department","type"]]
y = new_df['Rating']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

param_grid = {'alpha': [0.001, 0.01, 0.1, 1, 10]}
ridge = Ridge()
grid_search = GridSearchCV(ridge, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

print("Best Parameters:", grid_search.best_params_)

ridge_model = Ridge(alpha=grid_search.best_params_['alpha'])
ridge_model.fit(X_train, y_train)

y_pred = ridge_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Ridge Regression Mean Squared Error:", mse)

"""### Random Forest"""

from sklearn.ensemble import RandomForestRegressor

X = new_df[["Count","IssueDate","Department","type"]]
y = new_df['Rating']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

rf = RandomForestRegressor(n_estimators=100, max_depth=10)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Random Forest Mean Squared Error:", mse)

"""### SVM

"""

from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# Preprocess the data
X = new_df[["Count", "IssueDate", "Department", "type"]]
y = new_df['Rating']
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Define the model
svr = SVR()

# Define the parameter grid to search over
param_grid = {'kernel': ['linear', 'rbf', 'poly'],
              'C': [0.1, 1, 10],
              'epsilon': [0.01, 0.1, 1]}

# Use GridSearchCV to find the best hyperparameters
grid_search = GridSearchCV(svr, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)
print("Best Parameters:", grid_search.best_params_)

# Fit the model using the best hyperparameters
svr_model = SVR(kernel=grid_search.best_params_['kernel'], C=grid_search.best_params_['C'], epsilon=grid_search.best_params_['epsilon'])
svr_model.fit(X_train, y_train)

# Evaluate the model on the testing set
y_pred = svr_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Support Vector Regression Mean Squared Error:", mse)

"""### Neural networks"""

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from sklearn.metrics import mean_squared_error, r2_score

X = new_df[["Count","IssueDate","Department","type"]]
y = new_df['Rating']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = Sequential()
model.add(Dense(32, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(1, activation=None))
model.compile(loss='mean_squared_error', optimizer=Adam(lr=0.001))

model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("Neural Network R-squared Score:", r2)
print("Neural Network Mean Squared Error:", mse)

import pickle

filename='trained_model.sav'
pickle.dump(model,open(filename,'wb'))

#loading the saved model
loaded_modal=pickle.load(open("trained_model.sav", "rb"))

import pickle

# save the model to disk
filename = 'neural_network_model.sav'
pickle.dump(model, open(filename, 'wb'))

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))

# use the loaded model to make predictions
y_pred = loaded_model.predict(X_test)



