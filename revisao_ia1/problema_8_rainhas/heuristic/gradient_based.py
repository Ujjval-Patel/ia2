#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by lativ on 27/06/18 at 09:23

From: fizyka.umk.pl/~milosz/AlgIILab/10.1.1.57.4685.pdf
"""

import random

N = 8


def print_board(queens):
    line = ["_ "]*N
    for row in queens:
        line[row] = "Q "
        print("".join(line))
        line[row] = "_ "


def fill_diag_lines(queens, d1, d2):
    for row in range(N):
        d1[row + queens[row]] += 1
        d2[row - queens[row] + N - 1] += 1


def is_attacked(queens, d1, d2, row):
    if d1[row + queens[row]] > 1 or d2[row - queens[row] + N - 1] > 1:
        return True
    return False


def number_of_collisions(d1, d2):
    collisions = 0
    for line in range(2*N - 1):
        if d1[line] > 1:
            collisions += d1[line] - 1
        if d2[line] > 1:
            collisions += d2[line] - 1
    return collisions


def update_diags(queens, src, dst, d1, d2, op):
    d1[src + queens[src]] = op(d1[src + queens[src]], 1)
    d1[dst + queens[dst]] = op(d1[dst + queens[dst]], 1)
    d2[src - queens[src] + N - 1] = op(d2[src - queens[src] + N - 1], 1)
    d2[dst - queens[dst] + N - 1] = op(d2[dst - queens[dst] + N - 1], 1)


def swap(queens, src, dst, d1, d2):
    import operator
    update_diags(queens, src, dst, d1, d2, operator.sub)
    queens[src], queens[dst] = queens[dst], queens[src]
    update_diags(queens, src, dst, d1, d2, operator.add)


def queen_search(queens):
    swaps = None
    swaps_total = 0
    random.shuffle(queens)
    print('initial board: {}'.format(queens))
    d1 = [0 for _ in range(2*N - 1)]  # diagonal lines with size 2*N - 1
    d2 = d1.copy()
    fill_diag_lines(queens, d1, d2)
    # TODO: and in the case the queens shuffled has no solution?
    while swaps != 0:
        swaps = 0
        for i in range(N):
            for j in range(i+1, N):
                if is_attacked(queens, d1, d2, i) or is_attacked(queens, d1, d2, j):
                    collisions_before = number_of_collisions(d1, d2)
                    swap(queens, i, j, d1, d2)
                    swaps += 1
                    swaps_total += 1  # just to know
                    collisions_after = number_of_collisions(d1, d2)
                    if collisions_after >= collisions_before:
                        swap(queens, i, j, d1, d2)  # swap again; back to where it started
                        swaps -= 1
                        swaps_total -= 1

    print('board after {} swaps: {}'.format(swaps_total, queens))
    print()
    if N <= 32:
        print_board(queens)
        print()


if __name__ == '__main__':
    import time
    print("board size is {}".format(N))
    start = time.time()
    queen_search(list(range(N)))
    end = time.time()
    print("total time spent is {}s".format(end - start))
