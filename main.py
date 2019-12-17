import pandas as pd

from wordnet import SimilarWord
from wakati_document import wakati
from function import duplication, create_synonym_dictionary, create_word_dictionary
from random_delete import random_deletion
from random_insert import random_insertion
from random_swap import random_swap
from replace_synonym import synonym_replacement


if __name__ == '__main__':
    sw = SimilarWord()
    # jsonファイル読み込み
    df = pd.read_json('./document/train.jsonl', orient='records', encoding='utf-8', lines=True)
    data_list = df.values.tolist()
    word_type = ''
    # replace_synonym, random_insert用
    synonym_dictionary = create_synonym_dictionary(data_list, word_type, sw)
    # random_deletion用
    word_dictionary = create_word_dictionary(data_list, word_type)

    # 各手法の確率のパラメータ
    alpha_sr = 0.1
    p_rd = 0.1
    alpha_ri = 0.1
    alpha_rs = 0.1

    num_aug = 9
    num_new_per_technique = int(num_aug/4)+1

    # ダブり検知用の辞書
    sentence_list = {}
    num = 0

    for _ in range(10):
        with open('./document/all_approach/train_all_max.jsonl', 'a', encoding='utf-8') as json_file:
            for label, text in data_list:
                new_sentence = []
                all_wakati_word = wakati(text, '')
                wakati_word = wakati(text, word_type)

                # 各手法の確率
                num_words = len(wakati_word)
                n_sr = max(1, int(alpha_sr * num_words))
                n_ri = max(1, int(alpha_ri * num_words))
                n_rs = max(1, int(alpha_rs * num_words))

                new_sentence.append(synonym_replacement(text, wakati_word, synonym_dictionary, n_sr))
                new_sentence.append(random_deletion(all_wakati_word, word_dictionary, p_rd))
                new_sentence.append(random_insertion(all_wakati_word, wakati_word, synonym_dictionary, n_ri))
                new_sentence.append(random_swap(all_wakati_word, n_rs))
                print(new_sentence)

                for sentence in new_sentence:
                    sentence_dictionary = {"label": label, "text": sentence}
                    if duplication(sentence_list, num, sentence_dictionary['text']) is False:
                        json_file.write(str(sentence_dictionary).replace("'", '"') + '\n')
                        num += 1
