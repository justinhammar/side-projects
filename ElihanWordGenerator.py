#!/usr/bin/python
import random

def main():
    random.seed()

    vowels = ['e', 'i', 'u', 'o', 'a']
    prime_consonents = ['h', 'l', 'm', 'r', 'n', '']
    lesser_consonants = ['zh', 'sh', 'b', 'p', 'v', 'f', 'g', 'k', 'dh', 'th', 'd', 't', 'z', 's', 'y', 'w']
    all_consonants = list.copy(prime_consonents)
    all_consonants.extend(lesser_consonants)
    
    for x in range(100):
        first_letter = random.choice(all_consonants)
        middle_letter = random.choice(vowels)
        end_letter = random.choice(prime_consonents)
        
        syllable = first_letter + middle_letter + end_letter
        
        print(syllable + '\t', end='')
    

main()