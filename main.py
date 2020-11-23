import argparse
import logging
import os

import pandas as pd
from tqdm import tqdm

from EDA.random_delete import random_deletion
from EDA.random_insert import random_insertion
from EDA.random_swap import random_swap
from EDA.replace_synonym import synonym_replacement
from function import duplication, create_synonym_dictionary, create_word_dictionary
from wakati_document import wakati

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--target-path', type=str, default='document/sample.jsonl', help='target file path')
    parser.add_argument('--word-class', type=str, default='', help='proper_noun, noun, verb, adjective')
    parser.add_argument('--alpha-sr', type=float, help='parameter of alpha for synonym replace')
    parser.add_argument('--alpha-rd', type=float, help='parameter of alpha for random deletion')
    parser.add_argument('--alpha-ri', type=float, help='parameter of alpha for random insertion')
    parser.add_argument('--alpha-rs', type=float, help='parameter of alpha for random swap')
    parser.add_argument('--num-aug', type=int, default='9', help='number of augment per sentence')
    parser.add_argument('--num-exe', type=int, default='1', help='number of executions')

    opt = parser.parse_args()

    # jsonファイル読み込み
    df = pd.read_json(opt.target_path, orient='records', encoding='utf-8', lines=True)
    data_list = df.values.tolist()
    # replace_synonym, random_insert用
    synonym_dictionary = create_synonym_dictionary(data_list, opt.word_class)

    num_new_per_technique = int(opt.num_aug/4)+1

    # ダブり検知用の辞書
    sentence_list = {}
    num = 0
    # 保存ファイル用の名前抽出
    save_file_name = './document/{}_result.jsonl'.format(os.path.splitext(os.path.basename(opt.target_path))[0])
    with open(save_file_name, 'w', encoding='utf-8') as json_file:
        for i in range(opt.num_exe):
            logger.info(f'{i+1}回目の実行')
            for label, text in tqdm(data_list):
                new_sentence = []
                all_wakati_word = wakati(text, '')      # 全ての品詞を対象とした分かち書きリスト
                target_wakati_word = wakati(text, opt.word_class)      # ターゲットの品詞のみを分かち書きしたリスト
                num_words = len(target_wakati_word)
                if opt.alpha_sr is not None:
                    n_sr = max(1, int(opt.alpha_sr * num_words))
                    new_sentence.append(synonym_replacement(text, target_wakati_word, synonym_dictionary, n_sr))
                if opt.alpha_rd is not None:
                    new_sentence.append(random_deletion(all_wakati_word, target_wakati_word, opt.alpha_rd))
                if opt.alpha_ri is not None:
                    n_ri = max(1, int(opt.alpha_ri * num_words))
                    new_sentence.append(random_insertion(all_wakati_word, target_wakati_word, synonym_dictionary, n_ri))
                if opt.alpha_rs is not None:
                    n_rs = max(1, int(opt.alpha_rs * num_words))
                    new_sentence.append(random_swap(all_wakati_word, n_rs))

                for sentence in new_sentence:
                    sentence_dictionary = {"label": label, "text": sentence}
                    # 既に生成済みでない文章を保存する
                    if duplication(sentence_list, num, sentence_dictionary['text']) is False:
                        json_file.write(str(sentence_dictionary).replace("'", '"') + '\n')
                        num += 1
