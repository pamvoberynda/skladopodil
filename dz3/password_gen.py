import random as rand
from latinizer import latinize_word

punctuation_signs = ('!',',','?',':',';','.','—')
t16numbers = ('0','1','2','3',
              '4','5','6','7',
              '8','9','A','B',
              'C','D','E','F')

set_signs = punctuation_signs + t16numbers 

def create_password(word):
    word1 = latinize_word(word.lower())
    word = word1
    len_set = len(set_signs)
    created_passw = str()
    for letter in word:
        random_sign = rand.randint(0, len_set-1) 
        created_passw += set_signs[random_sign]
    return created_passw