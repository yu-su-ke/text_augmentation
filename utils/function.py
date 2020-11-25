from utils.wordnet import SimilarWord
from utils.wakati_document import wakati_text


def duplication(sentence_list, num, sentence):
    """ ダブった成分の検知

    Args:
        sentence_list (list): 既に生成済みの文章リスト
        num (int): 文章の生成回数
        sentence (str): 今回生成した文章

    Returns:
        boolean: 生成済みの文章だったらTrue、未生成の文章だったらFalse

    """
    if sentence not in sentence_list:  # 未登録なら
        sentence_list[sentence] = num
        return False
    else:
        return True


def create_synonym_dictionary(data_list, word_class):
    """ 同義語リストの作成

    Args:
        data_list (list): ラベルと文章セットのリスト
        word_class (str): 分かち書きする品詞の種類

    Returns:
        dict: 単語に対応する類義語の辞書

    """
    sw = SimilarWord()
    synonym_dict = {}
    for _, text in data_list:
        wakati_word = wakati_text(text, word_class)
        for word in wakati_word:
            synonym_list = sw.search_similar_word(word)
            if synonym_list is not None:
                if len(synonym_list) != 0:
                    synonym_dict[word] = synonym_list
    return synonym_dict
