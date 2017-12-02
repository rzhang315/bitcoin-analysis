from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
import math
import re
import glob
import os

def save_plot(name, original, predicted, look_back, future_offset):
    """
    Plot the prediction values and write vector image to file in the figures/ directory.

    Args:
        name      : name of the model, used as filename when writing to figures/
        original  : original dataset
        predicted : predicted dataset
        look_back : how many points to use in prediction
        future_offset : how many points into the future to shift the predicted outcome

    """
    # Shift predictions for plotting
    predict_plot = np.zeros(shape=(len(original), 1))
    predict_plot[:, :] = np.nan
    predict_plot[look_back + future_offset:len(predicted) + look_back + future_offset, :] = predicted

    # Plot original data with predictions
    plt.clf()
    plt.cla()
    plt.plot(original[:,0])
    plt.plot(predict_plot)
    plt.savefig('figures/{}.pdf'.format(name))

# Convert into dataset
def create_dataset(dataset, output_feature, look_back, future_offset):

    # Convert to numpy array and float values
    dataset = dataset.values
    dataset = dataset.astype('float32')

    # Get number of features
    _, num_features = dataset.shape

    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1 - future_offset):
        a = dataset[i:(i + look_back)].flatten()
        dataX.append(a)
        dataY.append(dataset[i + look_back + future_offset, output_feature])

    return np.array(dataX), np.array(dataY)

def main():

    # List of mode filenames
    models = []
    glob_str = 'model/model*.h5'
    for model_filename in glob.glob(glob_str):
        re_str = 'model\/model_L(.*)_F(.*)_TR(.*)_TS(.*).h5'
        match = re.search(re_str, model_filename)
        if match:
            models.append({
                'name': os.path.basename(os.path.splitext(model_filename)[0]),
                'look_back': int(match.group(1)),
                'future_offset': int(match.group(2)),
                'train_error': float(match.group(3)),
                'test_error': float(match.group(4)),
                'model': load_model(model_filename)
            })

    # Load dataset
    dataframe = read_csv('./data/bitcoin_historical_bitstamp.csv', usecols=[4], engine='python')

    # Truncate data
    dataframe = dataframe[3045000:]

    # Plot original data with predictions
    for model in models:
        input_vals, _ = create_dataset(dataframe, 0, model['look_back'], model['future_offset'])
        save_plot(model['name'], dataframe.values, model['model'].predict(input_vals), model['look_back'], model['future_offset'])

if __name__ == '__main__':
    main()