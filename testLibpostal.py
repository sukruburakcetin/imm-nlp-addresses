import flask
import re
from flask import Flask, render_template, request, flash
from postal.expand import expand_address
from postal.parser import parse_address

app = Flask(__name__)
app.secret_key = "imm-nlp-addresses-sukruburakcetin"

# print(parse_address("Mustafa Kemal Pasa Cadde Sirin sokagi No:1/5 Bahcelievler"))
# print(expand_address('Mustafa Kemal Pasa Sok ahmet cad'))

w = []  # words
with open('address_dictionary.txt', 'r', encoding="utf8") as f:
    file_name_data = f.read()
    file_name_data = file_name_data.replace('İ', 'i').lower()
    w = re.findall('\w+', file_name_data)

v = set(w)  # vocabulary

# print(f"The first 10 words in our dictionary are: \n{w[0:10]}")
# print(f"The dictionary has {len(v)} words ")

upper_map = {
    ord(u'ı'): u'I',
    ord(u'i'): u'İ'
}


# a get_count function that returns a dictionary of word vs frequency
def get_count(words):
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count


word_count = get_count(w)
print(f"The dictionary has  {len(word_count)} key values pairs")


# implement get_probs function
# to calculate the probability that any word will appear if randomly selected from the dictionary

def get_probs(word_count_dict):
    probs = {}
    m = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / m
    return probs


# Now we implement 4 edit word functions

# DeleteLetter:removes a letter from a given word
def DeleteLetter(word):
    delete_list = []
    split_list = []
    for i in range(len(word)):
        split_list.append((word[0:i], word[i:]))
    for a, b in split_list:
        delete_list.append(a + b[1:])
    return delete_list


# delete_word_l = DeleteLetter(word="cans")


# SwitchLetter:swap two adjacent letters
def SwitchLetter(word):
    split_l = []
    switch_l = []
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    switch_l = [a + b[1] + b[0] + b[2:] for a, b in split_l if len(b) >= 2]
    return switch_l


# switch_word_l = SwitchLetter(word="eta")


# replace_letter: changes one letter to another
def replace_letter(word):
    split_l = []
    replace_list = []
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    alphabets = 'abcçdefgğhıijklmnoöpqrsştuüvwxyz'
    replace_list = [a + l + (b[1:] if len(b) > 1 else '') for a, b in split_l if b for l in alphabets]
    return replace_list


# replace_l = replace_letter(word='can')


# insert_letter: adds additional characters
def insert_letter(word):
    split_l = []
    insert_list = []
    for i in range(len(word) + 1):
        split_l.append((word[0:i], word[i:]))
    letters = 'abcçdefgğhıijklmnoöpqrsştuüvwxyz'
    insert_list = [a + l + b for a, b in split_l for l in letters]
    # print(split_l)
    return insert_list


# combining the edits
# switch operation optional
def edit_one_letter(word, allow_switches=True):
    edit_set1 = set()
    edit_set1.update(DeleteLetter(word))
    if allow_switches:
        edit_set1.update(SwitchLetter(word))
    edit_set1.update(replace_letter(word))
    edit_set1.update(insert_letter(word))
    return edit_set1


# edit two letters
def edit_two_letters(word, allow_switches=True):
    edit_set2 = set()
    edit_one = edit_one_letter(word, allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = edit_one_letter(w, allow_switches=allow_switches)
            edit_set2.update(edit_two)
    return edit_set2


# edit three letters
def edit_three_letters(word, allow_switches=True):
    edit_set3 = set()
    edit_two = edit_two_letters(word, allow_switches=allow_switches)
    for z in edit_two:
        if z:
            edit_three = edit_one_letter(z, allow_switches=allow_switches)
            edit_set3.update(edit_three)
    return edit_set3


# get corrected word
def get_corrections(word, probs, vocab, n=3):
    suggested_word = []
    best_suggestion = []
    suggested_word = list(
        (word in vocab and word) or edit_one_letter(word).intersection(vocab) or edit_two_letters(word).intersection(
            vocab) or edit_three_letters(word).intersection(vocab))
    best_suggestion = [[s, probs[s]] for s in list(reversed(suggested_word))]
    return best_suggestion


@app.route("/nlp")
def index():
    flash("Hangi adres kelimesini sorgulamak istiyorsun?")
    return render_template("index.html")


@app.route("/nlpresult", methods=['POST', 'GET'])
def greeter():
    my_word = str(request.form['name_input'])
    probs = get_probs(word_count)
    tmp_corrections = get_corrections(my_word, probs, v, 3)
    for i, word_prob in enumerate(tmp_corrections):
        print(f"word {i}: {word_prob[0]}, probability {word_prob[1]:.6f}")
        result = (str(word_prob[0]).translate(upper_map)).upper()
    print("result: ", result)
    if result != "İ":
        flash("Sorgulanan kelimenin doğrusu " + result + ", sence de öyle mi?")
    return render_template("index.html")


@app.route("/")
def starting_url():
    return flask.redirect("/nlp")


app.config['JSON_AS_ASCII'] = False
app.run()
