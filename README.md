# EDA Text Augmentation
[EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks](https://arxiv.org/pdf/1901.11196.pdf)  
を参考に日本語の文章を対象としてText Augmentationを行う。  
行うタスクは、類義語置換・単語削除・単語スワップ・類義語挿入の4つである。  


## 環境構築
Python >= 3.7.0 でその他ライブラリのインストールは以下のコマンドを実行する。  
```shell script
$ pip install -r requirements.txt
```

wordnetのインストール
```shell script
$ cd database
$ sh download_wordnet.sh
```

documentフォルダの中に任意のjsonlファイルを保存する。  
jsonlファイルの形式は以下の通り。
```json
{"label": 0, "text": "(任意の文章)"}
{"label": 1, "text": "(任意の文章)"}
{"label": 2, "text": "(任意の文章)"}
︙
{"label": 1, "text": "(任意の文章)"}
```

上記の手順が済んだら以下のコマンドを実行する。  
処理の終了後にdocument内にresult.jsonlが保存される。
```shell script
python main.py --alpha-sr 0.1 --alpha-rd 0.1 --alpha-ri 0.1 --alpha-rs 0.1 --word-class noun
```


## 実行例
元文章
```
iPhoneには動画撮影機能が付いているが、その機能を使って動画を撮影し、それを投稿してみんなで楽しんでしまおうというSNSがあるので紹介しよう。
````

### 類義語置換(Replace Synonym)
単語をランダムに類義語で置換するタスク。  
類義語の候補はwordnetで帰ってきた単語の上位３件を候補とし、ランダムに選択している。

```
iPhoneには映像撮影機能が付いているが、その機能を使って映像を撮影し、それを投稿してみんなで楽しんでしまおうというSNSがあるので紹介しよう。
```

### 単語削除(Random Deletion)
文中から単語をランダムに削除するタスク。  
単語が一つしかない場合は削除しない。  
単語を全て削除してしまった場合は、文章からランダムに一つの単語を返す。

```
iPhone動画撮影機能動画撮影それ投稿みんなSNS紹介
```

### 単語スワップ(Random Swap)
文中の単語同士をランダムにスワップ(交換)するタスク。  
3回交換が行われなかった場合はそのまま返している。

```
iPhoneには動画撮影機能が付いているが、その機能を使って動画を撮影し、それを投稿してでで楽しんみんなしまおうというSNSがあるので紹介しよう。
```

### 類義語挿入(Random Insertion)
文中にある単語の類義語をランダムな場所に挿入するタスク。  
類義語の候補はwordnetで帰ってきた単語の上位３件を候補とし、ランダムに選択している。
```
絵そこiPhoneに絵は動画撮影機能が付いているが、その機能を使って動画を作動撮影し恭順、それを投稿して利く引合せるみんなで撮る撮る楽しんでしまおうというSNSがあるので紹介しよう。
```


## 参考文献
[1] J. Wei and K. Zou, "EDA: Easy data augmentation techniques for boosting performance on text classification tasks," Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pp. 6382–6388, 2019, doi: 10.18653/v1/d19-1670.  
[2] RONDHUIT Co, Ltd. "livedoor ニュースコーパス", https://www.rondhuit.com/download.html#ldcc .