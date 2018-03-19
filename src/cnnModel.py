# -*- coding:utf-8 -*-

import keras
import numpy
import sys


# 整理后, x的shape为(语料个数,height,width,通道数)  通道数:黑白为1, 彩色为3)
# 之所以height在前, 是因为m*n的图像是以行来输出,所以m在前
def preprocessImgData(x):
    shape = x.shape
    if len(shape) == 3:  # 黑白图片
        x = x.reshape(shape[0], shape[1], shape[2], 1)
    x = x.astype('float16')
    x /= 255
    return x


def toCategorical(y):
    num_classes = 1 + numpy.max(y)
    return keras.utils.to_categorical(y, num_classes)


batch_size = 32


def train(x_train, y_train, epochs, model_path):
    from keras.layers import Dense, Dropout, Activation, Flatten
    from keras.layers import Conv2D, MaxPooling2D
    from keras.models import Sequential

    num_classes = len(y_train[0])
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print('label num:', num_classes)

    model = Sequential()
    model.add(Conv2D(18, (3, 3), padding='same',
                     input_shape=x_train.shape[1:]))
    model.add(Activation('relu'))
    model.add(Conv2D(18, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(32, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes,name='preds'))

    model.add(Activation('softmax'))

    # initiate RMSprop optimizer
    opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

    # Let's train the model using RMSprop
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])

    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              shuffle=True,
              validation_split=0.1)
    # Save model and weights
    model.save(model_path)
    print('save model at %s ' % model_path)
    return model


def train2(x_train, y_train, epochs, model_path):
    from keras.layers import Dense, Dropout, Activation, Flatten
    from keras.layers import Conv2D, MaxPooling2D
    from keras.models import Sequential

    num_classes = len(y_train[0])
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print('label num:', num_classes)

    model = Sequential()

    model.add(Conv2D(32, (5, 5), padding='same',input_shape=x_train.shape[1:]))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (5, 5)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes,name='preds'))

    model.add(Activation('softmax'))

    # initiate RMSprop optimizer
    opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

    # Let's train the model using RMSprop
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])

    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              shuffle=True,validation_split=0.1)
    # Save model and weights
    model.save(model_path)
    print('save model at %s ' % model_path)
    return model


def test(model, x, y, epochs):
    print('test cases: '+str(len(x)))
    totalNum = x.shape[0]
    rightNum = 0
    res = model.predict(x, batch_size=epochs)
    res = numpy.argmax(res, axis=1)
    for i in range(totalNum):
        if res[i] == y[i]:
            rightNum += 1
    print('accuracy: ' + str('%.2f' % (rightNum / totalNum)))


def predict_on_batch(model, x):
    return model.predict_on_batch(x)


def loadModelFromFile(path):
    return keras.models.load_model(path)


def sizeOf(x):
    print(sys.getsizeof(x))
