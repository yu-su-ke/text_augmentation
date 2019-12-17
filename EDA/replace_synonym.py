import random
from random import shuffle

import pandas as pd

from wordnet import SimilarWord 
from wakati_document import wakati
from function import duplication, create_synonym_dictionary


def synonym_replacement(sentence, wakati_word, synonyms_dictionary, n):
    keys = synonyms_dictionary.keys()
    replace_sentence = sentence
    random.shuffle(wakati_word)
    num_replaced = 0
    for w in wakati_word:
        if w in keys:
            random_num = len(synonyms_dictionary[w])
            replace_sentence = replace_sentence.replace(w, synonyms_dictionary[w][random.randrange(random_num)])  
            # もし1番目の類義語に置換したかったらsynonyms_dictionary[w][0]にする  
            num_replaced += 1
        if num_replaced >= n: #only replace up to n words
            break
    return replace_sentence


if __name__ == '__main__':
    sw = SimilarWord()
    # jsonファイル読み込み
    df = pd.read_json('./document/train.jsonl', orient='records', encoding='utf-8', lines=True)
    data_list = df.values.tolist()
    word_type = '固有名詞'
    synonym_dict = create_synonym_dictionary(data_list, word_type, sw)

    alpha_sr = 0.1
    num_aug = 9
    num_new_per_technique = int(num_aug/4)+1

    # ダブり検知用の辞書
    sentence_list = {}
    num = 0

    for _ in range(1):
        with open('./document/replace_synonym/train_proper_noun.jsonl', 'a', encoding='utf-8') as json_file:
            for label, text in data_list:
                wakati_word = wakati(text, word_type)

                # 類義語置換の確率
                num_words = len(wakati_word)
                n_sr = max(1, int(alpha_sr*num_words))

                new_sentence = synonym_replacement(text, wakati_word, synonym_dict, n_sr)
                print(new_sentence)

                sentence_dictionary = {"label": label, "text": new_sentence}
                if duplication(sentence_list, num, sentence_dictionary['text']) is False:
                    json_file.write(str(sentence_dictionary).replace("'", '"') + '\n')
                    num += 1
