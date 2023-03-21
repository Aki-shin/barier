import time
import re
import pymorphy2

def init():
    f = open("banned words.txt", 'r', encoding='utf-8')
    global banned_words
    banned_words = f.read().split()
    morph = pymorphy2.MorphAnalyzer()
    result = []
    i = 0
    while i < len(banned_words):
        if banned_words[i][-1] == ':':
            result.append(banned_words[i].replace("_", " "))
            i += 1
        forms = morph.parse(banned_words[i])
        for form in forms:
            for x in form.lexeme:
                if (x.word not in result):
                    result.append(x.word)
        i += 1
    banned_words = result

def check_words(words):
    if isinstance(words, str):
        words = list(filter(None, re.split(";| |\.|,|\n", words)))
    words = list(map(str.lower, words))
    result = []
    category = ""
    i = 0
    while i < len(banned_words):
        if (banned_words[i][-1] == ':'):
            category = banned_words[i]
            i += 1
        j = 0
        find_flag = False
        if (banned_words[i] in words):
            result.append(category[:-1].replace("_", " "))
            find_flag = True
            j += 1
        if (find_flag):
            i = find_category(banned_words, i + 1)
        else:
            i += 1
    return result

def find_category(banned_words, i):
    j = i
    while (j < len(banned_words)):
        if (banned_words[j][-1] == ":"):
            return j
        else:
            j += 1
    return j

init()
inp = "я . уже. не могу. как что мне сделать,казино;блять, забирает все. мои   деньги, бля, порнуха ебаная, блять пиздец нахуй, как так то нахуй пидор гнойный я твой рот ебаллох спермобак"
answer = check_words(inp)
print(f"{answer}\n{len(banned_words)}")