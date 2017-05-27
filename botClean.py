#!/usr/bin/python

# Head ends here
import random

random.seed()

def choose_target(posr, posc, board):
    max_distance = 2 * (len(board[0]) - 1)
    for radius in range(max_distance + 1):
        spots_to_check = []
        for i in range(radius + 1):
            # add coordinates to a list without allowing duplicates
            if i == 0:
                spots_to_check.append((i, radius - i))
                spots_to_check.append((i, -(radius - i)))
            elif radius - i == 0:
                spots_to_check.append((i, radius - i))
                spots_to_check.append((-i, radius - i))
            else:
                spots_to_check.append((i, radius - i))
                spots_to_check.append((i, -(radius - i)))
                spots_to_check.append((-i, radius - i))
                spots_to_check.append((-i, -(radius - i)))
        # shuffle the list
        random.shuffle(spots_to_check)
        # iterate through list looking for a dirty square
        for x, y in spots_to_check:
            if posr + x < 0 or posc + y < 0 or posr + x >= len(board) or posc + y >= len(board[0]):
                continue
            if board[posr + x][posc + y] == 'd':
                return (posr + x, posc + y)
    else:
        # could not find a dirty square
        return (-1, -1)

def approach_target(posr, posc, targetr, targetc):
    delta_r = abs(posr - targetr)
    delta_c = abs(posc - targetc)
    if delta_r == 0 and delta_c == 0:
        return "HERE"
    move_likelihood = abs(delta_r / (delta_r + delta_c))
    if random.random() < move_likelihood:
        if posr > targetr:
            return "UP"
        else:
            return "DOWN"
    else:
        if posc > targetc:
            return "LEFT"
        else:
            return "RIGHT"

def next_move(posr, posc, board):
    r, c = choose_target(posr, posc, board)
    if r == -1:
        print("AREA ALL CLEAN. SHUTTING DOWN.")
    direction = approach_target(posr, posc, r, c)
    if direction == "HERE":
        print("CLEAN")
    else:
        print(direction)

# Tail starts here
if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)
