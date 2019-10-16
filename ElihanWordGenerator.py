#!/usr/bin/python
import random
import sys
import yaml

def main():
    random.seed()
    eh = Elihan()
    
    # with open('words.yml') as f:
        # word_list = yaml.safe_load(f)
    
    good_words = []
    for x in range(100):
        syllable_count = random.randint(2, 3)
        word = eh.create_word(syllable_count)
        #word = eh.create_world_name()
        print(f"{word:20}", end='')
        answer = input('')
        
        if answer is 'l':
            good_words.append(word)
        elif answer is 'q':
            print('----------------')
            for w in good_words:
                print(w)
            with open('elihan_words.yml', 'a') as f:
                yaml.dump(good_words, f)
            sys.exit()
        
        
class Elihan:
    def __init__(self):
        self.vowels = ['e', 'i', 'u', 'o', 'a']
        self.prime_consonents = ['h', 'l', 'm', 'r', 'n', '', '', '']
        self.lesser_consonants = ['zh', 'sh', 'b', 'p', 'v', 'f', 'g', 'k', 'dh', 'th', 'd', 't', 'z', 's', 'y', 'w', '\'']
        self.all_consonants = []
        self.all_consonants.extend(self.prime_consonents)
        self.all_consonants.extend(self.lesser_consonants)
        
        
    def create_syllable(self):
        first_letter = random.choice(self.all_consonants)
        middle_letter = random.choice(self.vowels)
        end_letter = random.choice(self.prime_consonents)
        
        return first_letter + middle_letter + end_letter
        
        
    def create_word(self, syllable_count):
        syllables = []
        for x in range(syllable_count):
            syllables.append(self.create_syllable())
        return ''.join(syllables)
        
    def create_world_name(self):
        elements_order = [1,2,3,4]
        random.shuffle(elements_order)
        
        world_name = []
        for x in elements_order:
            is_vowel_first = random.choice([True, False])
            if is_vowel_first:
                syllable = self.vowels[x] + self.prime_consonents[x]
            else:
                syllable = self.prime_consonents[x] + self.vowels[x]
            world_name.append(syllable)
            
        return ''.join(world_name)
        

main()
