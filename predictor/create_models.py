import numpy as np
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Flatten, Activation

"""
Create models to predict bitcoin prices.
"""

def generate_models(look_back, future_offset):

    def split_data(dataframe, look_back, future_offset):
        """
        Split data into training and testing sets

        Args:
            dataframe : pandas table for bitcoin prices
            look_back : number of consecutive points to use in prediction
            future_offset : how many points into the future to predict

        Returns:
            tuple of (train_x, train_y, test_x, test_y, num_features)

        """
        # Convert into dataset
        def create_dataset(dataset, output_feature):
            """
            Helper function to create dataset by combining the adjacent datapoints into a feature set.

            Args:
                dataset : numpy array of features
                output_feature : feature to predict into the future

            Returns:
                tuple of (data_x, data_y) numpy arrays
            """
            dataX, dataY = [], []
            for i in range(len(dataset) - look_back - 1 - future_offset):
                a = dataset[i:(i + look_back)].flatten()
                dataX.append(a)
                dataY.append(dataset[i + look_back + future_offset, output_feature])

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

        return train_x, train_y, test_x, test_y, num_features

    def create_and_train_model(train_x, train_y, test_x, test_y, num_features, look_back):
        """
        Create and train multilayer perceptron model.

        Args:
            train_x : numpy array of input values for training set
            train_y : numpy array of actualy y values for training set
            test_x  : numpy array of input values for test set
            test_y  : numpy array of actual y values to use in test validation
            num_features  : number of features used in prediction
            look_back : number of consecutive points to use in prediction

        Returns:
            model : keras model trained by the training data
            train_score : MSE score of training set
            test_score  : MSE score of test set
        """

        model = Sequential()
        layers = [1, 50, 100, 1]

        model.add(Dense(128, input_dim=look_back * num_features, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(1))

        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(train_x, train_y, epochs=300, batch_size=32, validation_split=0.10, verbose=2)

        # Estimate model performance
        train_score = model.evaluate(train_x, train_y, verbose=0)
        # print('Train Score: {0:.2f} MSE ({0:.2f} RMSE)'.format(train_score, math.sqrt(train_score)))
        test_score = model.evaluate(test_x, test_y, verbose=0)
        # print('Test Score: {0:.2f} MSE ({0:.2f} RMSE)'.format(test_score, math.sqrt(test_score)))

        return model, train_score, test_score

    # Seed with same number for reproducing same outcome
    np.random.seed(5)

    # Load dataset
    dataframe = read_csv('./data/bitcoin_historical_bitstamp.csv', usecols=[4], engine='python')

    # Truncate data
    dataframe = dataframe[3045000:]

    # Split data to train and test
    train_x, train_y, test_x, test_y, num_features = split_data(dataframe, look_back, future_offset)

    # Create model and train it
    model, train_score, test_score = create_and_train_model(train_x, train_y, test_x, test_y, num_features, look_back)

    # Save model to disk
    model.save('model/model_L{}_F{}_TR{}_TS{}.h5'.format(look_back, future_offset, train_score, test_score))


def main():
    # Look back and future offset pairs
    # look_back : number of datapoints to use to predict future
    # future_offset : number of items to predict into the future
    lb_fo_pairs = [(15, 5), (30, 15), (60, 30)]

    for look_back, future_offset in lb_fo_pairs:
        generate_models(look_back, future_offset)

if __name__ == '__main__':
    main()