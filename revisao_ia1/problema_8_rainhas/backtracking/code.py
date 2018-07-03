#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 22:16 2018

@author: lativ

from: https://www.geeksforgeeks.org/backtracking-set-3-n-queen-problem/
"""

global N
N = 10


def print_solution(board):
    for i in range(N):
        for j in range(N):
            print(board[i][j], end=' ')
        print('\n')


# nice func
def is_safe(board, row, col):
    for i in range(col):
        if board[row][i] == 1:
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True


def solve_n_queens_util(board, col):
    if col >= N:
        return True

    for i in range(N):
        if is_safe(board, i, col):
            board[i][col] = 1

            if solve_n_queens_util(board, col + 1):
                return True

            board[i][col] = 0

    return False


def solve_n_queens():
    board = [[0 for _ in range(N)] for _ in range(N)]

    if not solve_n_queens_util(board, 0):
        print("Solution does not exist.")
        return False

    print_solution(board)
    return True


if __name__ == '__main__':
    solve_n_queens()
