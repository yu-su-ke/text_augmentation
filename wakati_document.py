import MeCab
import re
import platform


def wakati(text, part):
    # print(text)
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
    # カウントからはじく単語を指定
    stop_words = [u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u'こと', u'これ', u'さん', u'して',
                  u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した', u'思う', u'ます',
                  u'それ', u'ここ', u'ちゃん', u'くん', u'って', u'て', u'に', u'を', u'は', u'の', u'が', u'と', u'た', u'し', u'で',
                  u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'から', u'けど',
                  'https', 't', '.', '/', '://', 'co', '@', '_', 'http',
                  '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                  '()', '！']
    while node:
        if node.surface != "":  # ヘッダとフッタを除外
            if part == '名詞':
                word_type = node.feature.split(",")[0]
                if word_type in [part] and node.surface not in stop_words:
                    output.append(node.surface)
            elif part == '動詞':
                word_type = node.feature.split(",")[0]
                if word_type in [part] and node.surface not in stop_words:
                    output.append(node.surface)
            elif part == '形容詞':
                word_type = node.feature.split(",")[0]
                if word_type in [part] and node.surface not in stop_words:
                    output.append(node.surface)
            elif part == '固有名詞':
                word_type = node.feature.split(",")[1]
                if word_type in [part] and node.surface not in stop_words:
                    output.append(node.surface)
                # word_type2 = node.feature.split(",")[2]
                # if word_type in ["人名", "地域"] and node.surface not in stop_words:
                #   output.append(node.surface)
                # elif word_type in ["組織"] and node.surface.isalpha() is False:
                #     output.append(node.surface)
            elif part == '':
                if node.surface not in stop_words:
                    output.append(node.surface)
        node = node.next
        if node is None:
            break

    # print(output)
    # 戻り値：list型
    return output


def format_text(text):
    text = re.sub(r'[!-~]', "", text)
    return text
