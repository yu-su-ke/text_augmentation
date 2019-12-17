import pandas as pd


def sdgs():
    df_tokyo = pd.read_json('./data/external/sdgs/utokyo_1.jsonl', orient='records', lines=True)
    df_okayama = pd.read_json('./data/external/sdgs/uokayama_1.jsonl', orient='records', lines=True)
    df_jst = pd.read_json('./data/external/sdgs/jst_1.jsonl', orient='records', lines=True)

    label_tokyo = [df_tokyo['label'][i] for i in range(len(df_tokyo))]
    text_tokyo = df_tokyo['text'].values.tolist()
    label_okayama = [df_okayama['label'][i] for i in range(len(df_okayama))]
    text_okayama = df_okayama['text'].values.tolist()
    label_jst = [df_jst['label'][i] for i in range(len(df_jst))]
    text_jst = df_jst['text'].values.tolist()
    
    create_dictionary(df_tokyo, label_tokyo, text_tokyo)
    create_dictionary(df_okayama, label_okayama, text_okayama)
    create_dictionary(df_jst, label_jst, text_jst)


def create_dictionary(df, label, text):
    with open('./data/external/sdgs/concat.jsonl', 'a') as json_file:
        for i in range(len(df)):
            print(i)
            clean_text = preprocess(text[i])
            sentence_dictionary = {"label": label[i], "text": clean_text}
            json_file.write(str(sentence_dictionary).replace("'", '"') + '\n')
        print('Done')


def sdgs_label_count():
    df = pd.read_json('./document/train.jsonl', orient='records', lines=True)
    label = df['label'].values.tolist()
    for i in range(1, 19):
        count = 0
        for j in range(len(label)):
            if label[j] == i:
                count += 1
        percent = count / len(df)
        print('label {} : {}個 : 割合 {}'.format(i, count, percent))
    print(len(df))


def shuffle_data():
    df = pd.read_json('./data/external/sdgs/document/train_proper_noun.jsonl', orient='records', lines=True)
    df_s = df.sample(frac=1, random_state=0).reset_index(drop=True)
    label = [df_s['label'][i] for i in range(len(df_s))]
    text = [df_s['text'][i] for i in range(len(df_s))]
    with open('./data/external/sdgs/concat.jsonl', 'w') as json_file:
        for i in range(len(df)):
            sentence_dictionary = {"label": label[i], "text": text[i]}
            json_file.write(str(sentence_dictionary).replace("'", '"') + '\n')


if __name__ in '__main__':
    # sdgs()
    sdgs_label_count()
    # shuffle_data()
