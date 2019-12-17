from wakati_document import wakati


# ダブった成分の検知
def duplication(sentence_list, num, sentence):
    if sentence not in sentence_list:  # 未登録なら
        sentence_list[sentence] = num
        return False
    else:
        print(sentence)
        return True


# 品詞別リストの作成
def create_word_dictionary(data_list, word_type):
    word_dict = {}
    for _, text in data_list:
        wakati_word = wakati(text, word_type)
        for word in wakati_word:
            if word != None:
                word_dict[word] = word
    return word_dict


# 同義語リストの作成
def create_synonym_dictionary(data_list, word_type, sw):
    synonym_dict = {}
    for _, text in data_list:
        wakati_word = wakati(text, word_type)
        print(wakati_word)
        for word in wakati_word:
            synonym_list = sw.search_similar_word(word)
            if synonym_list != None:
                if len(synonym_list) != 0:
                    synonym_dict[word] = synonym_list
    return synonym_dict

