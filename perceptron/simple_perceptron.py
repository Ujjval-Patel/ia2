#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by lativ on 28/08/18 at 21:48

Simulating the AND logical operator.

After, I've modified the data set to 'recognize' triangles inside. But the dimensions were low: (3, 3).
This implies low valid cases: only 4.

In this case we must expand the dimensions, like (6, 6) and insert a matrix (3, 3) that contains the triangle.

"""

import numpy as np
import time
import random


def activation(net):
    if net > 0:
        return 1
    else:
        return 0


def train_perceptron(X, Y, learning_rate=0.5):

    W = np.zeros_like(X[0])  # Get initial weights

    # INFO
    cicle = 0

    print("Initial weights: {}".format(W))

    same_weights = False

    while not same_weights:
        cicle += 1
        print("Cicle {}".format(cicle))

        n_input = 0

        same_weights = True

        for (x_in, y_out) in zip(X, Y):
            n_input += 1
            print('\tInput {}'.format(n_input))

            y_in = activation(np.dot(x_in, W))

            if y_in != y_out:
                weights_updated = []
                for (w, x) in zip(W, x_in):
                    wi = w + learning_rate * (y_out - y_in) * x
                    weights_updated.append(wi)

                W = np.asarray(weights_updated)

                same_weights = False

            print('\t\tWeights: {}'.format(W))

    return W


def get_and_operator_data():

   #           bias x1 x2
   X = np.array([[1, 0, 0],
                 [1, 0, 1],
                 [1, 1, 0],
                 [1, 1, 1]], np.uint8)

   Y = np.array([0, 0, 0, 1])

   return X, Y


def generate_triangles(mat_size, t_type):

    valid_triangle = np.array([[1, 0, 0], [1, 1, 0], [1, 1, 1]])
    invalid_triangle = np.array([[1, 1, 1], [0, 1, 1], [0, 0, 1]])
    triangle_size = 3

    triangles = []
    triangle = valid_triangle.copy()
    t_class = 1

    if t_type == 'invalid':
        triangle = invalid_triangle.copy()
        t_class = 0

    # Because we use a 5x5 matrix,
    # we only can insert triangles at (0, 0) to (idx_limit, idx_limit)
    idx_limit = mat_size - triangle_size
    idxs = []

    # TODO: is there a better way?
    for i in range(idx_limit + 1):
        for j in range(idx_limit + 1):
            idxs.append((i, j))

    # random.shuffle(idxs)

    # number of triangles is the total of possible coordinates
    n_triangles = idx_limit + 1
    n_triangles = n_triangles * n_triangles

    for _ in range(n_triangles):
        i, j = idxs.pop()
        mat = np.zeros((mat_size, mat_size), np.uint8)
        mat[i:i+3, j:j+3] = triangle.copy()
        mat = np.append(mat.ravel(), t_class)
        # triangles.append((mat.ravel(), t_class))
        triangles.append(mat)

    return triangles


def get_triangle_data():
    """
    A valid triangle here has the form:
        1 0 0
        1 1 0   that as a column vector is 1 0 0 1 1 0 1 1 1
        1 1 1

    A invalid triangle here has the form:
        1 1 1
        0 1 1   that as a column vector is 1 1 1 0 1 1 0 0 1
        0 0 1


    """

    # Return triangles as vectors with associated class (0 or 1) at the end.
    valid_triangle_list = generate_triangles(mat_size=5, t_type='valid')
    invalid_triangle_list = generate_triangles(mat_size=5, t_type='invalid')

    # Shuffle each triangle position
    random.shuffle(valid_triangle_list)
    random.shuffle(invalid_triangle_list)

    # Divide the list in half to train and half to test
    training_valid_triangles = valid_triangle_list[:len(valid_triangle_list)//2]
    test_valid_triangles = valid_triangle_list[len(valid_triangle_list)//2:]

    # Same for invalid triangles
    training_invalid_triangles = invalid_triangle_list[:len(invalid_triangle_list)//2]
    test_invalid_triangles = invalid_triangle_list[len(invalid_triangle_list)//2:]

    # Join lists of valid and invalid triangles for training. After, shuffle again.
    # X_train = np.concatenate([training_valid_triangles, training_invalid_triangles])
    X_train = training_valid_triangles + training_invalid_triangles
    random.shuffle(X_train)

    # Same for testing
    # X_test = np.concatenate([test_valid_triangles, test_invalid_triangles])
    X_test = test_valid_triangles + test_invalid_triangles
    random.shuffle(X_test)

    train_bias = np.ones((len(X_train), 1), np.uint8)
    test_bias = np.ones((len(X_test), 1), np.uint8)

    X_train = np.concatenate([train_bias, X_train], axis=1)
    Y_train = [t[-1] for t in X_train]
    X_train = np.delete(X_train, X_train.shape[1] - 1, axis=1)

    X_test = np.concatenate([test_bias, X_test], axis=1)
    Y_test = [t[-1] for t in X_test]
    X_test = np.delete(X_test, X_test.shape[1] - 1, axis=1)

    return X_train, Y_train, X_test, Y_test


def predict(test_in, weights):

    y_pred = activation(np.dot(test_in, weights))

    return y_pred


def test_perceptron(X, Y, weights):

    correct_classifications = 0

    for (x_in, y_out) in zip(X, Y):
        y_pred = activation(np.dot(x_in, weights))
        if y_pred == y_out:
            correct_classifications += 1

    return correct_classifications/len(X)

if __name__ == '__main__':

    # X, Y = get_and_operator_data()
    X_train, Y_train, X_test, Y_test = get_triangle_data()  # Both are numpy matrices

    trained_weights = train_perceptron(X_train, Y_train)

    timestr = time.localtime()
    timestr = '_'.join([str (t) for t in [timestr.tm_mday, timestr.tm_mon, timestr.tm_hour, timestr.tm_min]])
    np.save('weights_' + timestr, trained_weights)

    acc = test_perceptron(X_test, Y_test, trained_weights)

    print('accuracy: ', acc)
