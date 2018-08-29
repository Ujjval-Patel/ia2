#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by lativ on 28/08/18 at 21:48

Simulating the AND logical operator.
"""

import numpy as np


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


def get_triangle_data():

    """          X       Y
    001
    011  -> 001 011 111  1
    111

    (1, 3) (2, 2) (3, 1)

    100
    110  -> 100 110 111  1
    111

    (1, 1) (2, 1) (3, 1)

    111
    110  -> 111 110 100  1
    100

    (3, 1) (2, 1) (1, 1)

    111
    011  -> 111 011 001  1
    001

    """

    ones1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    ones2 = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]
    ones3 = [[1, 1, 1]]

    X = np.array([np.array([ones1[0], ones2[0], ones3[0]]).ravel(),  # y = 1
                  np.array([ones1[2], ones2[2], ones3[0]]).ravel(),  # y = 1
                  np.array([ones1[0], ones2[1], ones3[0]]).ravel(),  # y = 0
                  np.array([ones1[0], ones2[2], ones3[0]]).ravel(),  # y = 0
                  np.array([ones3[0], ones2[0], ones1[0]]).ravel(),  # y = 1
                  np.array([ones3[0], ones2[2], ones1[2]]).ravel(),  # y = 1
                  np.array([ones3[0], ones2[1], ones1[1]]).ravel(),  # y = 0
                  np.array([ones3[0], ones2[1], ones1[2]]).ravel(),  # y = 0
                  ], np.uint8)

    Y = np.array([1, 1, 0, 0, 1, 1, 0, 0])

    return X, Y


def predict(test_in, weights):

    y_pred = activation(np.dot(test_in, weights))

    return y_pred


if __name__ == '__main__':

    # X, Y = get_and_operator_data()
    X, Y = get_triangle_data()

    ones1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    ones2 = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]
    ones3 = [[1, 1, 1]]

    # This problem has the disadvantage of low valid cases
    # It is needed to re-think the input matrix X to allow more valid cases.
    test_in = np.array([ones2[0], ones3[0], ones1[0]]).ravel()
    test_out = 0

    trained_weights = train_perceptron(X, Y)
    y_pred = predict(test_in, trained_weights)
    print("\nInput: {}\nPredicted: {}\nActual: {}\n".format(test_in, y_pred, test_out))
