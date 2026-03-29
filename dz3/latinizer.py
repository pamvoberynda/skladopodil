
def latinize_letter(letter):
    accordance = (("й", "j"),("ц", "c"),("у", "u"),("к", "k"),
                  ("н", "n"),("г", "h"),("ґ", "g"),("ю", "ju"),
                  ("з", "z"),("ф", "f"),("і", "i"),("в", "v"),
                  ("а", "a"),("п", "p"),("р", "r"),("о", "o"),
                  ("д", "d"),("є", "je"),("я", "ja"),("ї","ji"),
                  ("л", "l"),("е", "e"),("ь", "j"),("т", "t"),
                  ("с", "s"),("м", "m"),("и", "y"),("б","b"),
                  ("ж", "zh"),("х", "kh"),("ш", "sh"),("ч", "ch"),
                  ("щ", "shch"))
    for tuplee in accordance:
      if letter == tuplee[0]:
        letter = tuplee[1]               
    return letter


def latinize_word(word):
    latinized_word = str()
    for letter in word:
        latinized_word += latinize_letter(letter)
    return latinized_word