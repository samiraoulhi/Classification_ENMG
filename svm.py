# -*- coding: utf-8 -*-
"""SVM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oBfieSxmLMqmAN8xevHTBxo8RhEEWDu5
"""

# Commented out IPython magic to ensure Python compatibility.
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay, accuracy_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from google.colab import drive
drive.mount('/content/drive')

path='/content/drive/MyDrive/Dataset/dataset3.csv'
df=df = pd.read_csv(path, delimiter=';')

df.head()

df0=df[df.Label=="Normal"]
df1=df[df.Label=="Mild"]
df2=df[df.Label=="Moderate"]
df3=df[df.Label=="Severe"]

# Define a mapping from labels to numbers
label_mapping = {'Normal': 0, 'Mild': 1, 'Moderate': 2, 'Severe':3}

# Map the labels to numbers using the defined mapping
df['target'] = df['Label'].map(label_mapping)
# Handle missing values by imputing with the mean
imputer = SimpleImputer(strategy='mean')

X = df.drop(['target','Label'], axis='columns')
y = df.target
# Split the data into training and testing sets, ensuring stratification to include all classes
X = imputer.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123, stratify=y)

from sklearn.svm import SVC
model = SVC(C=0.01, kernel='linear', class_weight='balanced')
model.fit(X_train, y_train)

# Evaluate the model using cross-validation for a more robust performance estimate
cross_val_scores = cross_val_score(model, X_train, y_train, cv=8)
print(f'Cross-validation scores: {cross_val_scores}')
print(f'Average cross-validation score: {cross_val_scores.mean()}')

# Evaluate the model on the test set
test_score = model.score(X_test, y_test)
print(f'Model accuracy on test set: {test_score}')

# Generate predictions on the test set
y_pred = model.predict(X_test)
y_pred

# Display the confusion matrix
cm = confusion_matrix(y_test, y_pred, normalize='true')
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_mapping.keys())
disp.plot()
plt.show()

# Display the classification report
print(classification_report(y_test, y_pred, target_names=label_mapping.keys()))

# Define a range of values for the parameter C
C_values = np.logspace(-3, 3, 7)  # Example range: from 0.001 to 1000

# Lists to store accuracy and cross-validation scores
accuracies = []
cv_scores = []

# Loop through each value of C
for C in C_values:
    # Create SVM model with linear kernel and current C value
    model = SVC(C=C, kernel='linear')

    # Perform cross-validation and compute mean accuracy
    cross_val_acc = cross_val_score(model, X_train, y_train, cv=9)
    mean_cv_acc = np.mean(cross_val_acc)

    # Evaluate model accuracy on test set
    model.fit(X_train, y_train)
    test_acc = model.score(X_test, y_test)

    # Append accuracy and cross-validation scores to lists
    accuracies.append(test_acc)
    cv_scores.append(mean_cv_acc)

# Plot results
plt.figure(figsize=(12, 6))

# Plot model accuracy and average cross-validation score as a function of C
plt.subplot(1, 2, 1)
plt.semilogx(C_values, accuracies, label='Model Accuracy (Test Set)', marker='o')
plt.semilogx(C_values, cv_scores, label='Average Cross-Validation Score', marker='s')
plt.xlabel('C (Regularization Parameter)')
plt.ylabel('Score')
plt.title('Model Performance vs. C (SVM with Linear Kernel)')
plt.legend()
plt.grid(True)

# Define a range of values for the number of folds (cv)
cv_values = range(2, 11)  # Example range: from 2 to 10

# Lists to store accuracy and cross-validation scores
accuracies = []
cv_scores = []

# Loop through each value of cv
for cv in cv_values:
    # Create SVM model with linear kernel and default C value
    model = SVC(C=0.01,kernel='linear')

    # Perform cross-validation and compute mean accuracy
    cross_val_acc = cross_val_score(model, X_train, y_train, cv=cv)
    mean_cv_acc = np.mean(cross_val_acc)

    # Evaluate model accuracy on test set
    model.fit(X_train, y_train)
    test_acc = model.score(X_test, y_test)

    # Append accuracy and cross-validation scores to lists
    accuracies.append(test_acc)
    cv_scores.append(mean_cv_acc)

# Plot model accuracy and average cross-validation score as a function of cv
plt.subplot(1, 2, 2)
plt.plot(cv_values, accuracies, label='Model Accuracy (Test Set)', marker='o')
plt.plot(cv_values, cv_scores, label='Average Cross-Validation Score', marker='s')
plt.xlabel('Number of Folds (CV)')
plt.ylabel('Score')
plt.title('Model Performance vs. Number of Folds (SVM with Linear Kernel)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()