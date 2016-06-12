from keras.models import Sequential
from keras.layers.core import Dense, Activation

# for a single-input model with 2 classes (binary):
model = Sequential()
model.add(Dense(1, input_dim=4, activation='softmax'))
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# generate dummy data
import numpy as np
data = np.random.random((1000, 4))
labels = np.random.randint(2, size=(1000, 1))

# train the model, iterating on the data in batches
# of 32 samples
model.fit(data, labels, nb_epoch=3, batch_size=32)
loss_and_metrics = model.evaluate(data, labels)
print loss_and_metrics
test = np.random.random((3, 4))
print model.predict_classes(test, batch_size=32, verbose=0)
