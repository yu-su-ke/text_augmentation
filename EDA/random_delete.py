import random
from random import shuffle

import pandas as pd

from wakati_document import wakati
from function import duplication, create_word_dictionary


def random_deletion(all_wakati_word, word_dictionary, p):
    keys = word_dictionary.keys()
    # 1単語の場合は削除しない
    if len(all_wakati_word) == 1:
        return all_wakati_word[0]

    # pの確率によって削除する
    new_words = []
    for w in all_wakati_word:
        if w in keys:
            r = random.uniform(0, 1)
            if r > p:
                new_words.append(w)
        new_words.append(w)

    # 全ての単語を削除した場合、1単語だけ返す
    if len(new_words) == 0:
        rand_int = random.randint(0, len(all_wakati_word)-1)
        return all_wakati_word[rand_int]

    sentence = ''.join(new_words)

    return sentence


if __name__ == '__main__':
    # jsonファイル読み込み
    df = pd.read_json('./document/train.jsonl', orient='records', encoding='utf-8', lines=True)
    data_list = df.values.tolist()
    word_type = ''
    word_dict = create_word_dictionary(data_list, word_type)

    p_rd = 0.1

    # ダブり検知用の辞書
    sentence_list = {}
    num = 0

    for _ in range(10):
        with open('./document/random_deletion/train_all_max.jsonl', 'a', encoding='utf-8') as json_file:
            for label, text in data_list:
                all_wakati_word = wakati(text, '')

                new_sentence = random_deletion(all_wakati_word, word_dict, p_rd)
                print(new_sentence)
                
                sentence_dictionary = {"label": label, "text": new_sentence}
                if duplication(sentence_list, num, sentence_dictionary['text']) is False:
                    json_file.write(str(sentence_dictionary).replace("'", '"') + '\n')
                    num += 1
