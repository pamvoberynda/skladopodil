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
        if index < lenght-1 and word[index+1] == word[index] and word[index] not in golosni:
            dig_word += "3"
            continue
        if index > 0 and word[index] == word[index-1] and word[index] not in golosni:
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
            next_syll = next_syll = raw_syllables[i + 1] if has_next else []
            if 4 not in next_syll and 5 not in curr_syll: # 24 | 25 -> 2425 
                curr_syll.extend(next_syll)
                done_syllables.append(curr_syll)
                i +=2
                continue
            if 2 in curr_syll:
                if len(curr_syll) == 1 and i-1 >= 0: # 24 | 2 -> 242
                    curr_syll.extend(prev_syll)
                    curr_syll.extend(curr_syll)
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
            if len(curr_syll) == 1 and curr_syll[0] not in (4,5): # 1 | 04 -> 104
                curr_syll.extend(next_syll)
                i+=1

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
    done_syllables = review_raw_syllables(raw_syllables)
    correlated_syllables = correlate_review_word(done_syllables, word)
    lenght = len(correlated_syllables)
    add_sep_idx = int()
    for syllable in correlated_syllables:
        output += syllable
        if add_sep_idx < lenght-1 and output[-1] in letters:
            output+= separator
        add_sep_idx+=1
    return output


worde = """Кольщик, наколи мені куполи,
Поруч — чудотворний хрест з іконами,
Щоб там дзвонили дзвони
З переливами та передзвонами.
 
Наколи мені будиночок біля струмка,
Нехай тече на волі тонкою цівкою.
Щоб від нього кравець-суддя
Не відгородив мене ґратами."""
print(separate_syllables(worde))