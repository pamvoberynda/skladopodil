# creates digitilized view of letters
gluhi = ("ц", "с", "к", "ф", "п", "т", "х", "ш", "ч", "щ") #0
dzvinki = ("д", "г", "ґ", "з", "б", "ж") #1
sonorni = ("й", "н", "м", "л", "р", "в", "`", "ʼ") #2
double_soft = ("ь",) #double sonorni or soft sign
golosni = ("а", "я", "о", "е", "є", "у", "ю", "и", "і", "ї") #4
#5 - space or unknown character etc
apostrof = ("`", "ʼ", "'") #5
letters = gluhi + dzvinki + sonorni + golosni + double_soft + apostrof

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
    lenght = len(raw_syllables)
    if lenght <= 1:
        return list(raw_syllables)

    done_syllables = []
    i = 0
    
    while i < lenght:
        curr_syll = list(raw_syllables[i])
        has_next = (i + 1 < lenght)
        next_syll = list(raw_syllables[i + 1]) if has_next else []
        prev_syll = done_syllables[-1] if done_syllables else []

        # 1. Логіка для сонорних (2)
        if 2 in curr_syll:
            if len(curr_syll) == 1 and prev_syll and prev_syll[-1] != 5: # 24 | 2 -> 242
                # Замість складної заміни, модифікуємо останній доданий склад
                done_syllables[-1].extend(curr_syll)
                i += 1
                continue
            elif len(curr_syll) == 2 and 3 in curr_syll:
                done_syllables[-1].extend(curr_syll)
                i += 1
                continue
            
            if len(curr_syll) == 1 and not prev_syll and has_next: # 2 | 42 -> 242
                next_syll = curr_syll + next_syll
                raw_syllables[i + 1] = next_syll # оновлюємо наступний
                i += 1
                continue

            if len(curr_syll) != 1 and prev_syll:
                for j in range(len(curr_syll) - 1):
                    if curr_syll[j] == 2 and curr_syll[j] == curr_syll[j+1]:
                        done_syllables[-1].append(curr_syll[j])
                        curr_syll.pop(0)
                        break

        # 2. Обов'язкова наявність голосної (4) у складі
        if 4 not in curr_syll:
            if has_next and 4 in next_syll and 5 not in (curr_syll[-1], next_syll[0]):
                # приєднуємо поточний безголосний до наступного
                raw_syllables[i + 1] = curr_syll + next_syll
                i += 1
                continue
            elif prev_syll and 4 in prev_syll:
                # приєднуємо поточний безголосний до попереднього фінального
                done_syllables[-1].extend(curr_syll)
                i += 1
                continue

        # 3. Поодинокі приголосні (1 | 04 -> 104)
        if len(curr_syll) == 1 and curr_syll[0] not in (4, 5): 
            if has_next: #1 | 04 -> 104
                raw_syllables[i + 1] = curr_syll + next_syll
                i += 1
                continue
            elif prev_syll: #14 | 0 -> 140
                done_syllables[-1].extend(curr_syll)
                i += 1
                continue

        # 4. Об'єднання відкритих складів (24 | 25 -> 2425)
        if has_next and 4 not in next_syll and 5 not in curr_syll and 3 not in next_syll and len(curr_syll) != 1:
            raw_syllables[i + 1] = curr_syll + next_syll
            i += 1
            continue

        # Якщо склад пройшов перевірки, додаємо його до фінальних
        done_syllables.append(curr_syll)
        i += 1

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
        if syllable[-1] in apostrof: #шоб імʼя показувало як ім-я, а не імʼя
            output+=syllable[:-1]
            add_sep_idx+=1
            output+= separator
            continue
        output += syllable
        if add_sep_idx < lenght-1 and output[-1] in letters:
            output+= separator
        add_sep_idx+=1
    return output


print("\tТекст:")
worde = """Ще зима не минула, я побачив тоді,
Як прекрасна дівчина посміхнулась мені.
Ми з тобою здружились, то були гарні дні,
Ми гуляли по парку, то було наче в сні.
 
І ти ніжною ходою та красою всіх зірок,
Сяйвом грації своєї, була кращою з жінок.
Ну, а погляд кришталевий, в моїм серці назавжди,
Ти в душі залишала слід від ніжної ходи."""
print(worde)
print("\tПриклад складоподілу:")
print(separate_syllables(worde))
print()