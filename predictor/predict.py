from keras.models import load_model
import numpy as np
from pandas import read_csv
import re
import glob
import os


def convert_to_model_input(dataset, look_back):
    """ Convert dataset input into a format understood by the model

    Args:
        dataset : original vector of values
        look_back : number of data points to look at for model

    Returns:
        dataset that has the values collapsed into a rolling set of size (look_back)
    """
    data_x = np.zeros(shape=(len(dataset) - look_back, look_back))
    for i in range(len(dataset) - look_back):
        data_x[i, :] = dataset[i:i + look_back].flatten()
    return data_x

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
        model_input_x = convert_to_model_input(input_vals, look_back)

        # Predict outcome
        predicted_vals = model.predict(model_input_x)
        predicted_vals = predicted_vals.flatten()
        return np.concatenate((np.zeros(shape=(look_back + future_offset)), predicted_vals), axis=0)
    else:
        raise ValueError("Model {} not found or improperly named".format(model_filename))

def main():

    # Load dataset
    dataframe = read_csv('./data/bitcoin_historical_bitstamp.csv', usecols=[4], engine='python')

    # Truncate data
    dataframe = dataframe[3045000:]

    # Convert to numpy array and float values
    dataset = dataframe.values
    dataset = dataset.astype('float32')

    prediction = predict('model/model_L15_F5_TR429.157226562_TS303.654984229.h5', dataset)

if __name__ == '__main__':
    main()