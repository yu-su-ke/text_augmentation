import random


def random_insertion(all_wakati_word, target_wakati_word, synonym_dictionary, n):
    """ 文章中の単語の類義語をランダムな位置に挿入する

    Args:
        all_wakati_word (list): 文章中の全ての単語リスト
        target_wakati_word (list): ターゲットの品詞のみの単語リスト
        synonyms_dictionary (dict): 特定の単語に対する類義語辞書
        n (int): タスク実行の回数上限

    Returns:
        str: タスク実行後の文章

    """
    new_words = all_wakati_word.copy()
    for _ in range(n):
        add_word(new_words, target_wakati_word, synonym_dictionary)

    new_sentence = ''.join(new_words)
    return new_sentence


def add_word(new_words, target_wakati_word, synonym_dictionary):
    keys = synonym_dictionary.keys()
    random.shuffle(target_wakati_word)
    for w in target_wakati_word:
        if w in keys:
            random_num = len(synonym_dictionary[w])
            random_synonym = synonym_dictionary[w][random.randrange(random_num)]  

            random_idx = random.randint(0, len(new_words)-1)
            new_words.insert(random_idx, random_synonym)
