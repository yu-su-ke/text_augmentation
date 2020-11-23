import random


def synonym_replacement(sentence, wakati_word, synonyms_dictionary, n):
    """ 単語を類義語で置換する

    Args:
        sentence (str): ターゲットとなる文章
        wakati_word (list): ターゲットの品詞のみを分かち書きしたリスト
        synonyms_dictionary (dict): 特定の単語に対する類義語辞書
        n (int): タスク実行の回数上限

    Returns:
        str: タスク実行後の文章

    """
    keys = synonyms_dictionary.keys()
    replace_sentence = sentence
    random.shuffle(wakati_word)
    num_replaced = 0
    for w in wakati_word:
        if w in keys:
            random_num = len(synonyms_dictionary[w])    # ターゲットの単語の類義語の個数
            replace_sentence = replace_sentence.replace(w, synonyms_dictionary[w][random.randrange(random_num)])
            # もし1番目の類義語に置換したかったらsynonyms_dictionary[w][0]にする  
            num_replaced += 1
        # タスクを上限回数まで実行
        if num_replaced >= n:
            break
    return replace_sentence
