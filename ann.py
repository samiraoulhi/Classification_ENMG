# -*- coding: utf-8 -*-
"""ANN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1h8sBOOMk8oY9Bmgff-q7Nwrl1-9Z-0bt
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import itertools
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from tensorflow.keras.models import Sequential
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Layer
from tensorflow.keras import regularizers
from sklearn.utils.class_weight import compute_class_weight
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from keras.utils import to_categorical
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils.class_weight import compute_class_weight
from sklearn.ensemble import RandomForestClassifier
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam, SGD, RMSprop, Adagrad, Adadelta, Nadam, AdamW

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Adjust the path to your file
file_path = '/content/drive/MyDrive/datasetV3.csv'

# Load the dataset
data= pd.read_csv(file_path, sep=';',header=None)
data.shape

# Load the dataset
data= pd.read_csv(file_path, sep=';',header=None)
# Drop the first row
data=data.drop(data.index[0])
# Write the updated DataFrame back to a file
data.to_csv('datasetV3.csv', index=False)
print(data.iloc[:, 25].unique())
#vérifier les classes cibles ou les étiquettes de classification dans les données.
data.iloc[:, 25].unique()
# Assuming the column you want to encode is column 36(adjust accordingly)
column_to_encode1 = data.iloc[:, 25]
# Initialize LabelEncoder
label_encoder = LabelEncoder()
# Fit label encoder and transform the column
encoded_column1 = label_encoder.fit_transform(column_to_encode1)
# Replace the original column with the encoded values
data.iloc[:, 25] = encoded_column1
print(data.iloc[:, 25].unique())
#for test data set
non_numeric_columns = data.select_dtypes(exclude=['number']).columns
print("Non-numeric columns:", non_numeric_columns)
data[non_numeric_columns] = data[non_numeric_columns].apply(pd.to_numeric, errors='coerce')
# Check for missing values after conversion
missing_values =data.isnull().sum()
# Remove rows with missing values
data= data.dropna()
# For example, fill missing values with mean
data= data.fillna(data.mean())
# Splitting data into Each Classes
df_1 = data[data[25] == 0]
df_2 = data[data[25] == 1]
df_3 = data[data[25] == 2]
df_4 = data[data[25] == 3]
#from sklearn.utils import resample
#df_1_upsample = resample(df_1, n_samples = 50, replace = True, random_state = 42)
#df_2_upsample = resample(df_2, n_samples = 50, replace = True, random_state = 42)
#df_3_upsample = resample(df_3, n_samples = 50, replace = True, random_state = 42)
#df_4_upsample = resample(df_4, n_samples = 50, replace = True, random_state = 42)
# merge and all dataframes to create new train samples
data = pd.concat([df_1, df_2, df_3, df_4])
x=data.iloc[:,:-1].values
# target Y
target_y =data[25]
data[25]
y = to_categorical(target_y)
#y= to_categorical(data)
#class_weights = compute_class_weight('balanced', classes=np.unique(target_y), y=target_y)
#class_weights = dict(enumerate(class_weights))
x=data.iloc[:,:-1].values
target_y =data[25]
y = to_categorical(target_y)
# Initialize the MinMaxScaler
scaler = MinMaxScaler()
# Fit the scaler to your data and transform your data
x= scaler.fit_transform(x)
#smote1 = SMOTE(random_state=42, k_neighbors=3)
#x,y= smote1.fit_resample(x, y)
# Diviser le dataset en train et temp (80 lignes pour train)
x_train,x_temp,y_train,y_temp = train_test_split(x, y, train_size=80,random_state=42 ,stratify=y)
# Diviser le reste (X_temp et y_temp) en test et validation
x_test, x_val, y_test, y_val = train_test_split(x_temp, y_temp,test_size=0.50,random_state=42, stratify=y_temp)

print(f'Taille de l\'ensemble d\'entraînement: {len(x_train)}')  # Devrait être 80
print(f'Taille de l\'ensemble de validation: {len(x_val)}')
print(f'Taille de l\'ensemble de test: {len(x_test)}')
len(x_temp)

# Choisissez un optimiseur
optimizer = Adam(learning_rate=0.01)
#optimizer = SGD(learning_rate=0.01, momentum=0.9)
#optimizer = RMSprop(learning_rate=0.001)
#optimizer = Adagrad(learning_rate=0.01)
#optimizer = Adadelta(learning_rate=1.0)
#optimizer = Nadam(learning_rate=0.001)
#optimizer = AdamW(learning_rate=0.001, weight_decay=0.01)
def build_model(learning_rate=0.01):
    model = Sequential()
    # kernel_regularizer=l2(0.01)
    model.add(Flatten()) # Flatten
    # Fully connected layer
    # input layer
    model.add(Dense(units=64, activation='relu',  input_shape=(25,)))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    # Hidden Layer
    model.add(Dense(units =32, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    # Hidden Layer
    model.add(Dense(units =16, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    # Hidden Layer
    model.add(Dense(units =8, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
     # Adjust the dropout rate as needed
    # Output Layer
    model.add(Dense(units = 4, activation='softmax'))
    model.compile(optimizer = optimizer, loss = 'categorical_crossentropy', metrics = ['accuracy'])
    return model
    model.summary()
model = build_model(learning_rate=0.01)
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
history = model.fit(x_train, y_train, epochs =250, batch_size =16,validation_data=(x_val, y_val),verbose=1, callbacks=[early_stopping])
#history = model.fit(x_train, y_train, epochs =250, batch_size =16,validation_data=(x_val, y_val),class_weight=class_weights)
# evaluate EMG Test Data
model.evaluate(x_test, y_test)
# converting hsitory to dataframe
pd.DataFrame(history.history)
pd.DataFrame(history.history)[['accuracy', 'val_accuracy']].plot().grid(True)
pd.DataFrame(history.history)[['loss','val_loss']].plot().grid(True)

#Make Prediction
predict = model.predict(x_test)


# Predicted o/p will be in probability distribution
predict
# distributional probability to integers
yhat = np.argmax(predict, axis = 1)
from sklearn.metrics import classification_report, confusion_matrix
confusion_matrix(np.argmax(y_test, axis = 1), yhat)
#plt.figure(figsize=(8,6))
#sns.heatmap(confusion_matrix(np.argmax(y_test, axis =1), yhat), annot = True, fmt = '0.0f', cmap= 'RdPu')

print(classification_report(np.argmax(y_test, axis=1), yhat))
print( model.summary())

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

cnf_matrix = confusion_matrix(np.argmax(y_test, axis = 1), yhat, normalize='true')
np.set_printoptions(precision=2)
# Plot non-normalized confusion matrix
plt.figure(figsize=(10, 10))
plot_confusion_matrix(cnf_matrix, classes=['Mild', 'Moderate', 'Normal', 'Severe'],normalize=True,
                      title='Confusion matrix, with normalization')
plt.show()