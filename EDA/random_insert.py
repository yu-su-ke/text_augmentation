import random
from random import shuffle

import pandas as pd

from wordnet import SimilarWord
from wakati_document import wakati
from function import create_synonym_dictionary, duplication


def random_insertion(sentence, wakati_word, synonym_dictionary, n):
    new_words = sentence.copy()
    for _ in range(n):
        add_word(new_words, wakati_word, synonym_dictionary)

    new_sentence = ''.join(new_words)
    return new_sentence


def add_word(new_words, wakati_word, synonym_dictionary):
    keys = synonym_dictionary.keys()
    random.shuffle(wakati_word)
    for w in wakati_word:
        if w in keys:
            random_num = len(synonym_dictionary[w])
            random_synonym = synonym_dictionary[w][random.randrange(random_num)]  

            random_idx = random.randint(0, len(new_words)-1)
            new_words.insert(random_idx, random_synonym)


if __name__ == '__main__':
    sw = SimilarWord()
    # jsonファイル読み込み
    df = pd.read_json('./document/train.jsonl', orient='records', encoding='utf-8', lines=True)
    data_list = df.values.tolist()
    word_type = ''
    synonym_dictionary = create_synonym_dictionary(data_list, word_type, sw)

    alpha_ri = 0.1

    # ダブり検知用の辞書
    sentence_list = {}
    num = 0

    for _ in range(10):
        with open('./document/random_insertion/train_all_max.jsonl', 'a', encoding='utf-8') as json_file:
            for label, text in data_list:
                all_wakati_word = wakati(text, '')
                wakati_word = wakati(text, word_type)

                # 類義語置換の確率
                num_words = len(wakati_word)
                n_ri = max(1, int(alpha_ri*num_words))

                new_sentence = random_insertion(all_wakati_word, wakati_word, synonym_dictionary, n_ri)
                print(new_sentence)

                sentence_dictionary = {"label": label, "text": new_sentence}
                if duplication(sentence_list, num, sentence_dictionary['text']) is False:
                    json_file.write(str(sentence_dictionary).replace("'", '"') + '\n')
                    num += 1
