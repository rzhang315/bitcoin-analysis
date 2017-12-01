# Predict bitcoin price of future time using sliding window
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Flatten, Activation

# Global parameters
LOOK_BACK = 15
FUTURE_OFFSET = 5

# Split into train and test set
def split_data(dataframe):
    def normalize_window(window):
        return [((float(p) / float(window[0])) - 1) for p in window]
    # Convert into dataset
    def create_dataset(dataset, output_feature):
        dataX, dataY = [], []
        for i in range(len(dataset) - LOOK_BACK - 1 - FUTURE_OFFSET):
            a = dataset[i:(i + LOOK_BACK)].flatten()
            dataX.append(a)
            dataY.append(dataset[i + LOOK_BACK + FUTURE_OFFSET, output_feature])

        return np.array(dataX), np.array(dataY)

    # Convert to numpy array and float values
    dataset = dataframe.values
    dataset = dataset.astype('float32')

    # Get number of features
    _, num_features = dataset.shape

    # Split to test and train
    train_size = int(len(dataset) * 0.7)
    test_size = len(dataset) - train_size
    train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

    # Generate feature set with predictions
    train_x, train_y = create_dataset(
        dataset=train,
        output_feature=0
    )
    test_x, test_y = create_dataset(
        dataset=test,
        output_feature=0
    )

    # TOOD: LSTM
    #train_x = np.reshape(train_x, (train_x.shape[0], train_x.shape[1], 1))
    #test_x = np.reshape(test_x, (test_x.shape[0], test_x.shape[1], 1))

    return train_x, train_y, test_x, test_y, num_features

def create_and_train_model(train_x, train_y, test_x, test_y, num_features):
    # Create and fit multilayer perceptron
    model = Sequential()

    layers = [1, 50, 100, 1]

    #model.add(LSTM(
    #    input_dim=layers[0],
    #    output_dim=layers[1],
    #    return_sequences=True))
    #model.add(Dropout(0.2))

    #model.add(LSTM(
    #    layers[2],
    #    return_sequences=False))
    #model.add(Dropout(0.2))

    model.add(Dense(128, input_dim=LOOK_BACK * num_features, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1))
    #model.add(Dense(output_dim=layers[3]))
    #model.add(Activation("linear"))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(train_x, train_y, epochs=100, batch_size=32, validation_split=0.10, verbose=2)

    # Estimate model performance
    train_score = model.evaluate(train_x, train_y, verbose=0)
    print('Train Score: {0:.2f} MSE ({0:.2f} RMSE)'.format(train_score, math.sqrt(train_score)))
    test_score = model.evaluate(test_x, test_y, verbose=0)
    print('Test Score: {0:.2f} MSE ({0:.2f} RMSE)'.format(test_score, math.sqrt(test_score)))

    return model

def plot_all(dataset, train_predict, test_predict):
    # Shift train predictions for plotting
    train_predict_plot = np.zeros(shape=(len(dataset), 1))
    train_predict_plot[:, :] = np.nan
    train_predict_plot[LOOK_BACK + FUTURE_OFFSET:len(train_predict) + LOOK_BACK + FUTURE_OFFSET, :] = train_predict

    # Shift test predictions for plotting
    test_predict_plot = np.zeros(shape=(len(dataset), 1))
    test_predict_plot[:, :] = np.nan
    test_predict_plot[len(train_predict) + (LOOK_BACK * 2) + (FUTURE_OFFSET * 2):len(dataset) - 2, :] = test_predict

    # Plot original data with predictions
    plt.plot(dataset[:,0])
    plt.plot(train_predict_plot)
    plt.plot(test_predict_plot)
    plt.show()

def main():

    # Seed with same number for reproducing same outcome
    np.random.seed(5)

    # Load dataset
    dataframe = read_csv('./data/bitcoin_historical_bitstamp.csv', usecols=[4,5], engine='python')

    # Truncate data
    dataframe = dataframe[3045000:]

    # Split data to train and test
    train_x, train_y, test_x, test_y, num_features = split_data(dataframe)

    # Create model and train it
    model = create_and_train_model(train_x, train_y, test_x, test_y, num_features)

    # Generate predictions
    train_predict = model.predict(train_x)
    test_predict = model.predict(test_x)

    # Plot original data with predictions
    plot_all(dataframe.values, train_predict, test_predict)

if __name__ == '__main__':
    main()