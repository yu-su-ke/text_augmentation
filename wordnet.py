import re

import sqlite3
import pandas as pd


class SimilarWord:
    def __init__(self):
        self.connection = sqlite3.connect("./wnjpn.db")  # データベース

    def search_similar_word(self, word):
        # 問い合わせた単語がWordnetに存在するかを確認する
        query = self.connection.execute("select wordid from word where lemma='%s'" % word)
        word_id = 99999999  # temp
        for row in query:
            word_id = row[0]
        if word_id == 99999999:
            print('「%s」は、Wordnetに存在しない単語です。' % word)
            # 存在しない場合は処理打ち切り
            return
        else:
            print('「%s」の類義語を出力します。' % word)

        # 存在する場合は単語を含む概念を検索する
        query_concept = self.connection.execute("select synset from sense where wordid='%s'" % word_id)
        concept_sets = []
        for row in query_concept:
            concept_sets.append(row[0])

        # 概念に含まれる単語を検索する
        number_concept = 1
        synonym_list = []
        for concept_set in concept_sets:
            # 概念検索
            search_concept = self.connection.execute("select name from synset where synset='%s'" % concept_set)
            for row1 in search_concept:
                print('%sつめの概念 : %s' % (number_concept, row1[0]))
            # 意味検索
            search_meaning = self.connection.execute("select def from synset_def where (synset='%s' and lang='jpn')" % concept_set)
            number_meaning = 1
            for row2 in search_meaning:
                print("意味%s : %s" % (number_meaning, row2[0]))
                number_meaning += 1
            # 類義語検索
            search_word = self.connection.execute("select wordid from sense where (synset='%s' and wordid!=%s)" % (concept_set, word_id))
            number_word = 1
            for row3 in search_word:
                target_word_id = row3[0]
                search_word_detail = self.connection.execute("select lemma from word where wordid=%s AND lang='jpn'" % target_word_id)
                for row3_1 in search_word_detail:
                    # 類義語から英語を弾いた上で上位5件のものを保存
                    if number_word <= 3:
                        print("類義語%s : %s" % (number_word, row3_1[0]))
                        synonym_list.append(row3_1[0])
                        number_word += 1

            print('\n')
            number_concept += 1
            # 最初の概念を読み込むとき
            # return synonym_list
        # 全ての概念を読み込む場合
        return synonym_list

    def similar_word(self, data):
        for word in data:
            # シングルクォーテーションを全角に(エラー回避)
            re.sub("'", "’", word)
            self.search_similar_word(word)


def synonym_replacement(sentence, wakati_word, synonyms_lexicon):
    keys = synonyms_lexicon.keys()
    n_sentence = sentence
    for w in wakati_word:
        if w in keys:
            n_sentence = n_sentence.replace(w, synonyms_lexicon[w][0])  # we replace with the first synonym
    return n_sentence


def create_synonym_dictionary(data_list):
    synonym_dict = {}
    for label, text in data_list:
        print(text)
        wakati_word = wakati(text, "固有名詞")
        for word in wakati_word:
            synonym_list = sw.search_similar_word(word)
            if synonym_list != None:
                if len(synonym_list) != 0:
                    synonym_dict[word] = synonym_list
    return synonym_dict


if __name__ == '__main__':
    sw = SimilarWord()
    # jsonファイル読み込み
    df = pd.read_json('./document/concat.jsonl', orient='records', encoding='utf-8', lines=True)
    data_list = df.values.tolist()
    synonym_dict = create_synonym_dictionary(data_list)

    for label, text in data_list:
        wakati_word = wakati(text, "固有名詞")
        new_sentence = synonym_replacement(text, wakati_word, synonym_dict)
        print(new_sentence)
