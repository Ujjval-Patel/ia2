#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 20:32:38 2018

@author: lativ

from: https://www.geeksforgeeks.org/branch-and-bound-set-4-n-queen-problem/
"""

N = 32


def print_solution(board):
    for i in range(N):
        for j in range(N):
            print("{} ".format(board[i][j]), end=' ')
        print("\n")
        

def is_safe(row, col, slash_code, backslash_code,
            row_lookup, slash_code_lookup, backlash_code_lookup):
    if (slash_code_lookup[slash_code[row][col]] or
            backlash_code_lookup[backslash_code[row][col]] or
            row_lookup[row]):
        return False
    return True


def solve_n_queens_util(board, col, slash_code,
                        backslash_code, row_lookup,
                        slash_code_lookup, backslash_code_lookup):
    if col >= N:
        return True

    for i in range(N):
        if is_safe(i, col, slash_code, backslash_code, row_lookup, slash_code_lookup, backslash_code_lookup):
            board[i][col] = 1
            row_lookup[i] = True
            slash_code_lookup[slash_code[i][col]] = True
            backslash_code_lookup[backslash_code[i][col]] = True

            if solve_n_queens_util(board, col + 1, slash_code,
                                   backslash_code, row_lookup,
                                   slash_code_lookup, backslash_code_lookup):
                return True

            board[i][col] = 0
            row_lookup[i] = False
            slash_code_lookup[slash_code[i][col]] = False
            backslash_code_lookup[backslash_code[i][col]] = False

    return False


def solve_n_queens():

    board = [[0 for _ in range(N)] for _ in range(N)]

    slash_code = [[None for _ in range(N)] for _ in range(N)]
    backslash_code = [[None for _ in range(N)] for _ in range(N)]

    row_lookup = [False for _ in range(N)]

    slash_code_lookup = [False for _ in range(2*N - 1)]
    backslash_code_lookup = [False for _ in range(2*N - 1)]

    for i in range(N):
        for j in range(N):
            slash_code[i][j] = i + j
            backslash_code[i][j] = i - j + N - 1

    if not solve_n_queens_util(board, 0, slash_code,
                               backslash_code, row_lookup,
                               slash_code_lookup, backslash_code_lookup):
        print("Solution does not exists.")
        return False

    print_solution(board)
    return True


if __name__ == '__main__':
    solve_n_queens()
