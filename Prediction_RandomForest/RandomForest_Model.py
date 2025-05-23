# import libraries
import numpy as np
import pandas as pd
import pickle  
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import warnings
warnings.filterwarnings('ignore')

# Load the downsampled dataset
data_downsampled = pd.read_csv("./Datasets/processed_dataset.csv")

# split dataset into features and target variable
X = data_downsampled.drop(columns=["rainfall"], axis=1)
y = data_downsampled["rainfall"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
RFC_model = RandomForestClassifier(random_state=42)


"""Training Model"""
# Define the parameter grid for RandomForestClassifier
param_grid_rf = {
    "n_estimators": [50, 100, 200],
    "max_features": ["sqrt", "log2"],
    "max_depth": [None, 10, 20, 30],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4]
}

# GridSearch with cross-validation to find the best hyperparameters
GridSearchCV_RFC = GridSearchCV(estimator=RFC_model, param_grid=param_grid_rf, cv=5, n_jobs=-1, verbose=2)
GridSearchCV_RFC.fit(X_train, y_train)

# output the best model from GridSearch
Best_RF_model = GridSearchCV_RFC.best_estimator_
print("Best parameters for Random Forest: ", GridSearchCV_RFC.best_params_)


"""Model Evaluation"""
# Perform cross-validation on the training set
cv_scores = cross_val_score(Best_RF_model, X_train, y_train, cv=5)
print("Cross-validation scores for Random Forest Classifier: ", cv_scores)
print("Mean cross-validation score for Random Forest Classifier: ", cv_scores.mean())

# Prediction the test set
y_pred = Best_RF_model.predict(X_test)

# evaluate model's accuracy on the test set
print("\nTest set Accuracy: ", accuracy_score(y_test, y_pred))
print("\nTest set Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
print("\nTest set Classification Report: \n", classification_report(y_test, y_pred))


"""Test on Random data"""
# Prediction on random data
random_data = (1021.8, 10.4, 78, 88, 20, 50.0, 28.8)

# Reshape the data to match the model's expected input
random_data = np.array(random_data).reshape(1, -1)

# Make a prediction using the best Random Forest model output from GridSearch
prediction = Best_RF_model.predict(random_data)

if prediction == 0:
    print("Prediction result: ", "No Rainfall")
else:
    print("Prediction result: ", "Rainfall")
    

# Save the model to a file
RF_model = {"model": Best_RF_model, "feature_names": X.columns.tolist()} 

with open("./Prediction_RandomForest/RandomForest_model.pkl", "wb") as file:
    pickle.dump(RF_model, file)

print("Model saved successfully!")
