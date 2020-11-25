import re
import sys

import emoji


def clean_text(text):
    """ 改行やタブ、タグを削除する

     Args:
         text (str): 文章

     Returns:
         str: タスク実行後の文章

     """
    x = str(text)
    x = x.replace('\n', '')  # 改行削除
    x = x.replace('\t', '')  # タブ削除
    x = x.replace('\r', '')
    # x = x.replace('年', '')
    # x = x.replace('月', '')
    # x = x.replace('日', '')
    # x = x.replace('時', '')
    x = re.sub(re.compile(r'[!-\/:-@[-`{-~]'), ' ', x)
    x = re.sub(r'\[math\]', ' LaTex math ', x)  # LaTex削除
    x = re.sub(r'\[\/math\]', ' LaTex math ', x)  # LaTex削除
    x = re.sub(r'\\', ' LaTex ', x)  # LaTex削除
    x = re.sub(r'(\d+)([a-zA-Z])', '\g<1> \g<2>', x)  # タグの削除
    x = re.sub(r'(\d+) (th|st|nd|rd) ', '\g<1>\g<2> ', x)  # タグの削除
    x = re.sub(r'(\d+),(\d+)', '\g<1>\g<2>', x)  # タグの削除
    x = re.sub(' +', ' ', x)  # 連続して出現する空白の削除
    return x


def rm_symbol(text):
    """ 特殊文字、記号などを削除する

     Args:
         text (str): 文章

     Returns:
         str: タスク実行後の文章

     """
    symbols = r',.":)・《》「」『』！(-!?|;\'$&/[]>%=#*+\\•~@£·_{}©^®`<→°€™›♥←×§″′Â█½à…“★”–●â►−¢²¬░¶↑±¿▾═¦║―¥▓—‹─▒：' \
             r'¼⊕▼▪†■’▀¨▄♫☆é¯♦¤▲è¸¾Ã⋅‘∞∙）↓、│（»，♪╩╚³・╦╣╔╗▬❤ïØ¹≤‡√。【】〜'
    for symbol in symbols:
        text = text.replace(symbol, '')
    return text


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '')


def rm_spaces(text):
    """ ユニコード文字などを削除する

    Args:
        text (str): 文章

    Returns:
        str: タスク実行後の文章

    """
    spaces = ['\u200b', '\u200e', '\u202a', '\u2009', '\u2028', '\u202c', '\ufeff', '\uf0d8', '\u2061', '\u3000',
              '\u200d', '\u0602', '\ue32e', '\U000feb0f', '´༎ຶ۝༎ຶ ', '۝', '\U000feb60', '\U0001f90d', '\U0001fa70',
              '\U0001f9cf', '\U0001fa90', '\U0001f9a6', '\U0001f9a9',
              '\U000e0067', '\U000e0062', '\U000e0065', '\U000e006e', '\U000e007f', '\U0001f9a5', '\U0001f9a6',
              '\ue14c', '⁦',
              '\x10', '\x7f', '\x9d', '\xad',
              '\x97', '\x9c', '\x8b', '\x81', '\x80', '\x8c', '\x85', '\x92', '\x88', '\x8d', '\x80', '\x8e', '\x9a',
              '\x94', '\xa0',
              '\x8f', '\x82', '\x8a', '\x93', '\x90', '\x83', '\x96', '\x9b', '\x9e', '\x99', '\x87', '\x84', '\x9f',
              '\x08', '\x0f',
              '\uf840', '\uf8ff', '\u200c', '\ue335', '\uf840', '\x0b', '\uf8be'
              ]
    for space in spaces:
        text = text.replace(space, ' ')
    text = text.translate(non_bmp_map)
    return text


def remove_emoji(text):
    """ 絵文字を削除する

    Args:
        text (str): 文章

    Returns:
        str: タスク実行後の文章

    """
    return ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)


def replace_num(text):
    """ 数字をアノニマス化する

    Args:
        text (str): 文章

    Returns:
        str: タスク実行後の文章

    """
    text = re.sub('[0-9]{5,}', '#####', text)
    text = re.sub('[0-9]{4}', '####', text)
    text = re.sub('[0-9]{3}', '###', text)
    text = re.sub('[0-9]{2}', '##', text)
    text = re.sub('[０-９]{5,}', '#####', text)
    text = re.sub('[０-９]{4}', '####', text)
    text = re.sub('[０-９]{3}', '###', text)
    text = re.sub('[０-９]{2}', '##', text)
    return text


def preprocess(text):
    text = rm_symbol(text)
    text = rm_spaces(text)
    text = clean_text(text)
    text = remove_emoji(text)
    text = replace_num(text)
    return text
