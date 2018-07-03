#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by lativ on 01/07/18 at 19:48
"""


# Steps (from wiki)

# Let s = s0
# For k = 0 through k_max (exclusive)
#   T <- temperature(k / k_max)
#   Pick a random neighbour, s_new <- neighbour(s)
#   If P(E(s), E(s_new), T) >= random(0, 1):
#       s <- s_new
# Output: the final state s

# Problems to resolve before trying:
#   - what is the temperature?
#   - acceptance probability P is that by Kirkpatrick et al., is that ok?
