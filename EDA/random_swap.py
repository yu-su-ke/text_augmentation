import random


def random_swap(all_wakati_word, n):
    """ ランダムに単語をスワップする

    Args:
        all_wakati_word (list): 文章中の全ての単語リスト
        n (int): タスク実行の回数上限

    Returns:
        str: タスク実行後の文章

    """
    new_words = all_wakati_word.copy()
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
    return new_words
