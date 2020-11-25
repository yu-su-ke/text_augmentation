import MeCab
import re
import platform


def wakati_text(text, word_class, stop_words=None):
    """ 文書を分かち書きする

    Args:
        text (str): 分かち書きする文章
        word_class (str): ターゲットとする品詞
        stop_words (list): 分かち書き時に弾くストップワード

    Returns:
        list: 分かち書きリスト

    """
    pf = platform.system()
    if pf == 'Windows':
        mecab = MeCab.Tagger('-Owakati')
    elif pf == 'Darwin':
        mecab = MeCab.Tagger("-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
    elif pf == 'Linux':
        mecab = MeCab.Tagger("-Owakati -d /usr/lib/mecab/dic/mecab-ipadic-neologd/")
    mecab.parse('')
    node = mecab.parseToNode(text)
    output = []
    if stop_words is None:
        stop_words = []
    # カウントからはじく単語を指定
    while node:
        if node.surface != "":  # ヘッダとフッタを除外
            if word_class == 'noun':
                word_type = node.feature.split(",")[0]
                if word_type in ['名詞'] and node.surface not in stop_words:
                    output.append(node.surface)
            elif word_class == 'verb':
                word_type = node.feature.split(",")[0]
                if word_type in ['動詞'] and node.surface not in stop_words:
                    output.append(node.surface)
            elif word_class == 'adjective':
                word_type = node.feature.split(",")[0]
                if word_type in ['形容詞'] and node.surface not in stop_words:
                    output.append(node.surface)
            elif word_class == 'proper_noun':
                word_type = node.feature.split(",")[1]
                if word_type in ['固有名詞'] and node.surface not in stop_words:
                    output.append(node.surface)
            elif word_class == '':
                if node.surface not in stop_words:
                    output.append(node.surface)
        node = node.next
        if node is None:
            break
    return output
