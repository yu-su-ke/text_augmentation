import os
import random

import pandas as pd

from format_text import preprocess


def read_text(path_list):
    sentence_label = []
    for p_list in path_list:
        path = "./document/" + p_list + '/'
        # ディレクトリ内の全ファイル名を取得
        f_list = os.listdir(path)
        for list in f_list:
            with open(path + list, mode='r', encoding="utf-8") as f:
                # 1行目と2行目をスキップ
                next(f)
                next(f)
                # 全角スペースや改行の削除
                w = preprocess(f.read())

                label = path_list.index(p_list)
                sentence_label.append([label, w])
    create_jsonl(sentence_label)


def create_jsonl(sentence_label):
    sentence_label_shuffle = random.sample(sentence_label, len(sentence_label))
    train_index = 4426
    dev_index = 5901
    test_index = len(sentence_label_shuffle)
    index_list = [0, train_index, dev_index, test_index]
    file_name = ['train', 'dev', 'test']
    try:
        for i in range(3):
            with open('./document/' + file_name[i] + '.jsonl', encoding='utf-8', mode='w') as json_file:
                for data in sentence_label_shuffle[index_list[i]:index_list[i+1]]:
                    sentence_dictionary = {"label": data[0], "text": data[1]}
                    json_file.write(str(sentence_dictionary).replace("'", '"') + '\n')
            print('Done')
    except TypeError as e:
        print(e)


def livedoor_label_count():
    df = pd.read_json('./document/train.jsonl', encoding='utf-8', orient='records', lines=True)
    label = df['label'].values.tolist()
    for i in range(0, 9):
        count = 0
        for j in range(len(label)):
            if label[j] == i:
                count += 1
        percent = count / len(df)
        print('label {} : {}個 : 割合 {}'.format(i, count, percent))
    print(len(df))


if __name__ in '__main__':
    # ファイルの読み込み、及びタイトル・本文データの取得
    path_list = ["dokujo-tsushin", "it-life-hack", "kaden-channel", 'livedoor-homme', 'movie-enter', 'peachy',
                 'smax', 'sports-watch', 'topic-news']
    read_text(path_list)
    # livedoor_label_count()
