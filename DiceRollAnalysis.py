#!/usr/bin/python
import random

random.seed()

def main():
    # d20AdvEmp(100000)
    # d20AdvThe()
    # emp3d6Adv(100000)
    the3d6Adv()
    
def emp3d6Adv(sets):
    reg = [0]*19
    adv = [0]*19
    
    for i in range(sets):
        d6_1 = random.randint(1, 6)
        d6_2 = random.randint(1, 6)
        d6_3 = random.randint(1, 6)
        d6_4 = random.randint(1, 6)
        regResult = d6_1 + d6_2 + d6_3
        minRoll = min(d6_1, d6_2, d6_3, d6_4)
        advResult = d6_1 + d6_2 + d6_3 + d6_4 - minRoll
        
        reg[regResult] += 1
        adv[advResult] += 1
        
    printDiceStatsTable(sets, 1, 18, reg, adv)
    
    
def the3d6Adv():
    reg = [0]*19
    adv = [0]*19
    
    for i in range(1, 6 + 1):
        for j in range(1, 6 + 1):
            for k in range(1, 6 + 1):
                for l in range(1, 6 + 1):
                    regResult = i + j + k
                    minRoll = min(i, j, k, l)
                    advResult = i + j + k + l - minRoll
                    reg[regResult] += 1
                    adv[advResult] += 1
                    
    average = avgProb(pow(6, 4), 1, 18, adv)
    
    printDiceStatsTable(pow(6, 4), 1, 18, reg, adv)
    
    print('average advantage roll =', average)
    

def d20AdvEmp(sets):
    adv = [0]*21
    reg = [0]*21

    for i in range(sets):
        d20_1 = random.randint(1, 20)
        d20_2 = random.randint(1, 20)
        result = max(d20_1, d20_2)
        
        adv[result] += 1
        reg[d20_1] += 1
        
    printDiceStatsTable(sets, 1, 20, reg, adv)
    

def d20AdvThe():
    adv = [0]*21
    reg = [0]*21

    for i in range(1, 20 + 1):
        for j in range(1, 20 + 1):
            result = max(i, j)
            adv[result] += 1
            reg[i] += 1
            
    average = avgProb(400, 1, 20, adv)
        
    printDiceStatsTable(400, 1, 20, reg, adv)
    
    print('average advantage roll =', average)
    
    
def avgProb(sets, low, high, adv):
    sum = 0
    for i in range(low, high + 1):
        sum += adv[i] * i
    return sum / sets
    
    
def printDiceStatsTable(sets, low, high, reg, adv):
    # print the results in a table
    print('|  # | Reg (%) | Adv (%) |')
    print('--------------------------')
    for i in range(low, high + 1):
        print('|', repr(i).rjust(2), '|', end=' ')
        print(repr(round(reg[i] / sets * 100, 2)).rjust(7), '|', end=' ')
        print(repr(round(adv[i] / sets * 100, 2)).rjust(7), '|')
    print('--------------------------')
        
        
main()