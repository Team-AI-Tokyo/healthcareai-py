"""This file is used to create and compare two models on a particular dataset.
It provides examples of reading from both csv and SQL Server. Note that this
example can be run as-is after installing healthcare.ai. After you have
found that one of the models works well on your data, move to Example2
"""
import pandas as pd
import time

import healthcareai.common.file_io_utilities as io
import healthcareai.pipelines.data_preparation as pipelines
from healthcareai.simple_mode import SimpleDevelopSupervisedModel

# Start a timer
t0 = time.time()

# CSV snippet for reading data into dataframe
dataframe = pd.read_csv('healthcareai/tests/fixtures/DiabetesClincialSampleData.csv', na_values=['None'])

# Drop columns that won't help machine learning
dataframe.drop(['PatientID', 'InTestWindowFLG'], axis=1, inplace=True)

# TODO what about the test window flag - can we deprecate it?

# Look at the first few rows of your dataframe after the data preparation
print(dataframe.head())

# Step 1: Setup healthcareai for developing a regression model.
hcai = SimpleDevelopSupervisedModel(
    dataframe,
    'SystolicBPNBR',
    'regression',
    impute=True,
    grain_column='PatientEncounterID')

# Train the linear regression model
trained_linear_model = hcai.linear_regression()
print('Model trained in {} seconds'.format(time.time() - t0))

# Once you are happy with the result of the trained model, it is time to save the model.
saved_model_filename = 'linear_regression_2017-04-18.pkl'
io.save_object_as_pickle(saved_model_filename, trained_linear_model)
print('model saved as {}'.format(saved_model_filename))

# TODO swap out fake data for real databaes sql
prediction_dataframe = pd.read_csv('healthcareai/tests/fixtures/DiabetesClincialSampleData.csv', na_values=['None'])

# Drop columns that won't help machine learning
columns_to_remove = ['PatientID', 'InTestWindowFLG']
prediction_dataframe.drop(columns_to_remove, axis=1, inplace=True)

# Run through the preparation pipeline
prediction_dataframe = pipelines.dataframe_prediction(
    prediction_dataframe,
    'regression',
    'PatientEncounterID',
    'SystolicBPNBR',
    impute=True)

# Load the saved model
linear_model = io.load_saved_model(saved_model_filename)
print('Model loaded. Type: {}'.format(type(linear_model)))

# Make some prections
predictions = linear_model.predict(prediction_dataframe)

# Save the predictions back to your dataframe
prediction_dataframe['SystolicBPNBR_predicted'] = predictions

# Peek at the predictions
print(prediction_dataframe.head())