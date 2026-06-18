# creates digitilized view of letters
gluhi = ("ц", "с", "к", "ф", "п", "т", "х", "ш", "ч", "щ") #0
dzvinki = ("д", "г", "ґ", "з", "б", "ж") #1
sonorni = ("й", "н", "м", "л", "р", "в") #2
double_soft = ("ь",) #double sonorni or soft sign
golosni = ("а", "я", "о", "е", "є", "у", "ю", "и", "і", "ї") #4
#5 - space or unknown character etc
letters = gluhi + dzvinki + sonorni + golosni + double_soft

def digitilize_word(word: str) -> str:
    dig_word = str()
    lenght = len(word)
    for index, letter in enumerate(word):
        if index < lenght-1 and word[index+1] == word[index] and word[index] in sonorni:
            dig_word += "3"
            continue
        if index > 0 and word[index] == word[index-1] and word[index] in sonorni:
            dig_word += "3"
            continue
        if letter in gluhi:
            dig_word += "0"
        elif letter in dzvinki:
            dig_word += "1"
        elif letter in sonorni:
            dig_word += "2"
        elif letter in golosni:
            dig_word += "4"
        elif letter in double_soft:
            dig_word += "3"
        else:
            dig_word += "5"
    return dig_word

def mk_raw_syllables(dig_word: str) -> list: # створюють склади за принципом, що кожен новий елемент складу має бути більшим за попередній
    raw_syllables = []
    dig_word = [int(letter) for letter in dig_word]
    lenght = len(dig_word)
    curr_syll = [dig_word[0]]

    for i in range(lenght-1):
        curr_dig = dig_word[i]
        next_dig = dig_word[i+1]
        if curr_dig > next_dig or (curr_dig == next_dig and curr_dig == 4): #either bigger number or new vowel
            raw_syllables.append(curr_syll)
            curr_syll = [next_dig]
        else:
            curr_syll.append(next_dig)
    if curr_syll:
        raw_syllables.append(curr_syll)

    return raw_syllables

def review_raw_syllables(raw_syllables: list) -> list:
    done_syllables = []
    lenght = len(raw_syllables)
    i = int()
    if lenght <= 1:
        return done_syllables.extend(raw_syllables)

    if lenght > 1:
        while i < lenght:
            has_next = i + 1 < lenght
            prev_syll = raw_syllables[i-1] if i != 0 else []
            curr_syll = raw_syllables[i]
            next_syll = raw_syllables[i + 1] if has_next else []
            print(f"curr is {curr_syll}")
            
            
            #if 3 in curr_syll and : # x | 3n | y -> x | 3n+y
            #    if 
            if 2 in curr_syll:
                if len(curr_syll) == 1 and i-1 >= 0: # 24 | 2 -> 242
                    curr_syll.extend(prev_syll)
                    curr_syll.extend(curr_syll) # <- 18.VI.26 на холеру це тут?
                    done_syllables.append(curr_syll)
                    curr_syll = next_syll
                if len(curr_syll) == 1 and i-1 <= 0: # 2 | 42 -> 242
                    curr_syll.extend(curr_syll)
                    curr_syll.extend(next_syll)
                    done_syllables.append(curr_syll)
                    curr_syll = next_syll
                
                if len(curr_syll) != 1 and i-1 >= 0: 
                    for j in range(len(curr_syll)-1):
                        cur_symb = curr_syll[j]
                        next_symb = curr_syll[j+1] 
                        if cur_symb == 2 and cur_symb == next_symb: # 24 | 2245 -> 242 | 245
                            prev_syll.append(cur_symb)
                            curr_syll.pop(0) 
                            break
            
            
            if 4 not in curr_syll: #prescribe logic of essential having vowel in a syllable: 24 | 13 | 143 -> 24 | 13143
                
                if next_syll and 4 in next_syll:
                    tempsyll = next_syll
                    next_syll = curr_syll
                    next_syll.extend(tempsyll)
                    raw_syllables[i + 1] = next_syll                   
                    i+=1
                    continue
                elif prev_syll and 4 in prev_syll:   
                    print("nigga")                 
                    tempsyll = prev_syll                    
                    prev_syll = curr_syll                    
                    tempsyll.extend(prev_syll)                
                    done_syllables[-1] = tempsyll               
                    i+=1
                    continue
            
            
            print(f"currrrr is {curr_syll}")
            if len(curr_syll) == 1 and curr_syll[0] not in (4,5) and next_syll != []: # 1 | 04 -> 104
                curr_syll.extend(next_syll)
                i+=1
            elif len(curr_syll) == 1 and curr_syll[0] not in (4,5) and next_syll == [] and prev_syll: # 14 | 0 -> 140
                tempsyll = prev_syll
                print(tempsyll)
                prev_syll = curr_syll
                print(prev_syll)
                tempsyll.extend(prev_syll)
                print(tempsyll)
                done_syllables[-1] = tempsyll
                print(done_syllables[-1])
                i+=1
                print(i)
                continue

            if 4 not in next_syll and 5 not in curr_syll and 3 not in next_syll and len(curr_syll) != 1: # 24 | 25 -> 2425 
                print(curr_syll)
                curr_syll.extend(next_syll)
                done_syllables.append(curr_syll)
                i +=2
                continue

            i+=1
            done_syllables.append(curr_syll)
            
        
    return done_syllables

def correlate_review_word(done_syllables: list, orig_word: str) -> list:
    done_word = []
    i = int()
    for subliste in done_syllables:
        step = len(subliste)
        done_word.append(orig_word[i:i+step])
        i+=step

    return done_word


def separate_syllables(word: str, separator="-"):
    output = str()
    word = word.lower()
    dword = digitilize_word(word)
    raw_syllables = mk_raw_syllables(dword)
    print("\t raw syllables:")
    for raw in raw_syllables:
        print(raw)
    done_syllables = review_raw_syllables(raw_syllables)
    print("\t done syllables:")
    for done in done_syllables:
        print(done)
    correlated_syllables = correlate_review_word(done_syllables, word)
    lenght = len(correlated_syllables)
    add_sep_idx = int()
    for syllable in correlated_syllables:
        output += syllable
        if add_sep_idx < lenght-1 and output[-1] in letters:
            output+= separator
        add_sep_idx+=1
    return output


worde = """руський русский руский Символом 
Символ найбільш мирних мирний мирні"""

worde = """найбільш"""
print(separate_syllables(worde))