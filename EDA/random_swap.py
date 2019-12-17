import random

import pandas as pd

from wakati_document import wakati
from function import duplication


def random_swap(words, n):
    new_words = words.copy()
    for _ in range(n):
        new_words = swap_word(new_words)
    sentence = ''.join(new_words)
    return sentence


def swap_word(new_words):
    random_idx_1 = random.randint(0, len(new_words)-1)
    random_idx_2 = random_idx_1
    counter = 0
    while random_idx_2 == random_idx_1:
        random_idx_2 = random.randint(0, len(new_words)-1)
        counter += 1
        if counter > 3:
            return new_words
    new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
    print('{}を{}と交換しました。'.format(new_words[random_idx_1], new_words[random_idx_2]))
    return new_words


if __name__ == '__main__':
    # jsonファイル読み込み
    df = pd.read_json('./document/train.jsonl', orient='records', encoding='utf-8', lines=True)
    data_list = df.values.tolist()
    word_type = ''

    alpha_rs = 0.1

    # ダブり検知用の辞書
    sentence_list = {}
    num = 0

    for _ in range(10):
        with open('./document/random_swap/train_swap_max.jsonl', 'a', encoding='utf-8') as json_file:
            for label, text in data_list:
                all_wakati_word = wakati(text, '')
                num_words = len(all_wakati_word)

                n_rs = max(1, int(alpha_rs*num_words))

                new_sentence = random_swap(all_wakati_word, n_rs)
                print(new_sentence)
                
                sentence_dictionary = {"label": label, "text": new_sentence}
                if duplication(sentence_list, num, sentence_dictionary['text']) is False:
                    json_file.write(str(sentence_dictionary).replace("'", '"') + '\n')
                    num += 1
