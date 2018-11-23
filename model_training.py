
import pandas as pd
import numpy as np


import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.models import Sequential, Model, load_model
from keras.layers import Activation, Dense, Dropout
from keras.callbacks import ModelCheckpoint, TensorBoard
import random
random.seed(1)
import warnings
warnings.filterwarnings('ignore')
import h5py




#read data
X = pd.read_hdf('data/X.h5').values
y = pd.read_hdf('data/y.h5').values.reshape(X.shape[0],-1)


# create training and test dataset
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.1)

# Model Hyperparameters
layer1_dense = X_train.shape[1]
layer2_dense = int(round(X_train.shape[1]*2))
layer3_dense = int(round(X_train.shape[1]*1))
layer4_dense = int(round(X_train.shape[1]*.5))

dropOut = (0.5, 0.5, 0.5, 0.5)
dense = (layer1_dense, layer2_dense, layer3_dense, layer4_dense)

# Training parameters
batchSize = 128
numEpochs = 10
valSplit = 0.1


model = Sequential()
model.add(Dense(dense[0], input_shape=(X_train.shape[1],), activation='relu'))
model.add(Dropout(dropOut[0]))
model.add(Dense(dense[1], activation='relu'))
model.add(Dropout(dropOut[1]))
model.add(Dense(dense[2], activation='relu'))
model.add(Dropout(dropOut[2]))
model.add(Dense(dense[3], activation='linear'))
model.add(Dropout(dropOut[3]))
model.add(Dense(y_train.shape[1]))
model.summary()

model.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['mse'])

tensorboard = TensorBoard(log_dir='./logs',
                          histogram_freq=0,
                          write_graph=True,
                          write_images=True)

checkpointer = ModelCheckpoint(filepath="models/NN_model.h5",
                               verbose=0,
                               save_best_only=True)

history = model.fit(X_train, y_train,
                    batch_size=batchSize,
                    epochs=numEpochs,
                    verbose=1,
                    validation_split = valSplit,
                    callbacks=[checkpointer, tensorboard]).history


#Plot learning curve to identify next steps in hyperparameter tuning
plt.plot(history['loss'])
plt.plot(history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper right')
plt.show()


predictions = model.predict(X_test)
true_prices = y_test
plt.scatter(true_prices,predictions, color = 'orange')
plt.plot([min(true_prices), max(true_prices)],[min(true_prices), max(true_prices)])
plt.title('mdoel validation')
plt.ylabel('true prices')
plt.xlabel('predicted prices')
plt.legend(['ideal prediction', 'model prediction'], loc='upper right')
plt.show()

mae_model = np.absolute(true_prices-predictions).mean()
mae_dummy = np.absolute(true_prices-y.mean()).mean()
print('Dummy model MAE: {:0.2f}\
\nTrained model MAE {:0.2f}'.format(mae_dummy, mae_model))
