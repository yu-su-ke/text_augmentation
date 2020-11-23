import random


def random_deletion(all_wakati_word, target_wakati_word,  p):
    """ ランダムに単語を削除する

    Args:
        all_wakati_word (list): 文章中の全ての単語リスト
        target_wakati_word (list): ターゲットの品詞のみの単語リスト
        p (float): タスク実行の確率

    Returns:
        str: タスク実行後の文章

    """
    # 1単語の場合は削除しない
    if len(all_wakati_word) == 1:
        return all_wakati_word[0]

    # pの確率によって削除する
    new_words = []
    for w in all_wakati_word:
        if w in target_wakati_word:
            r = random.uniform(0, 1)
            if r > p:
                new_words.append(w)

    # 全ての単語を削除した場合、1単語だけ返す
    if len(new_words) == 0:
        rand_int = random.randint(0, len(all_wakati_word)-1)
        return all_wakati_word[rand_int]

    sentence = ''.join(new_words)
    return sentence
