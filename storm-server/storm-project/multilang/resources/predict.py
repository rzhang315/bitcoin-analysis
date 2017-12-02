from keras.models import load_model
import numpy as np
from pandas import read_csv
import re
import glob
import os

def predict(model_filename, input_vals):
    """
    Give vector of prediction values based on input_vals and model.

    Args:
        model_filename : name of file to load the model (model/model_.*.h5)
        input_vals : numpy array of values to send to model
    """

    # Check if file exists and has properly formatted name
    re_str = 'model\/model_L(.*)_F(.*)_TR(.*)_TS(.*).h5'
    match = re.search(re_str, model_filename)
    if os.path.isfile(model_filename) and match is not None:

        # Load parameters and model
        look_back = int(match.group(1))
        future_offset = int(match.group(2))
        model = load_model(model_filename)

        # Convert input data to one that can be fed to model
        model_input_x = input_vals

        # Predict outcome
        predicted_vals = model.predict(model_input_x)
        predicted_vals = predicted_vals.flatten()
        return predicted_vals[0]
    else:
        raise ValueError("Model {} not found or improperly named".format(model_filename))

