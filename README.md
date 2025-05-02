# Emotional Text to Speech

感情表現を含むテキストを音声に変換するアプリケーションです。
https://github.com/litagin02/Style-Bert-VITS2 に対して、以下のような追加を行っています

- docker run でFastAPIサーバとして音声合成サーバが立ち上がるようにEntrypoint設定
- 音声合成に利用するモデルを事前ダウンロードするためのスクリプト `model_download/initialize_x.py` を追加
    - ダウンロードするファイル数、サイズが大きく、ネットワークエラーになりやすい。1つのスクリプトで全ファイルをダウンロードすると、ネットワークエラー時に最初からやり直しになるため、複数スクリプトでダウンロードを行い、エラーが発生しても途中から再開できるようにした

## Base Repository
[Style-Bert-VITS2の2025/3/29時点のmasterブランチ](https://github.com/litagin02/Style-Bert-VITS2/commit/1d7a7a0d484d56eebe99c5fd88a9ba52091b87bd)をCloneしています

## How to use

```
# build
docker build -t style-bert-vits2-webapi .

# run
docker run --rm -it -p 5000:5000 style-bert-vits2-webapi
...
(しばらく起動に時間がかかるので待つ)
...
05-02 12:31:15 |  INFO  | server_fastapi.py:335 | server listen: http://127.0.0.1:5000
05-02 12:31:15 |  INFO  | server_fastapi.py:336 | API docs: http://127.0.0.1:5000/docs
05-02 12:31:15 |  INFO  | server_fastapi.py:337 | Input text length limit: 100. You can change it in server.limit in config.yml

# ブラウザで http://localhost:5000/docs にアクセスするとAPIドキュメントが確認できる
```

### curlコマンドでのAPI呼び出し

```
# 利用可能なモデル一覧を取得
curl -X 'GET' \
  'http://localhost:8000/models/info' \
  -H 'accept: application/json'

{
  "0": {
    "config_path": "model_assets/jvnv-M1-jp/config.json",
    "model_path": "model_assets/jvnv-M1-jp/jvnv-M1-jp_e158_s14000.safetensors",
    "device": "cpu",
    "spk2id": {
      "jvnv-M1-jp": 0
    },
    "id2spk": {
      "0": "jvnv-M1-jp"
    },
    "style2id": {
      "Neutral": 0,
      "Angry": 1,
      "Disgust": 2,
      "Fear": 3,
      "Happy": 4,
      "Sad": 5,
      "Surprise": 6
    }
  },
  ...
}
```

```
# 音声合成
# 音声合成に使うモデル名, model_assets内のディレクトリ名
MODEL_NAME=jvnv-F1-jp
# 話者ID。model_assets>[model]>config.json内のspk2idを確認
SPEAKER_ID=0
# 生成したいテキストを指定
TARGET_TEXT="こんにちわ！"

# WebAPIに渡すテキストはURLエンコードしている必要があるため、pythonのurllib.parseを使ってエンコード
ENCODED_TEXT=`python -c "import urllib.parse; import sys; print(urllib.parse.quote(sys.argv[1]))" ${TARGET_TEXT}`

# あるいは、「こんにちわ！」をURLエンコードした値は以下なので利用ください
ENCODED_TEXT="%E3%81%93%E3%82%93%E3%81%AB%E3%81%A1%E3%82%8F%EF%BC%81%EF%BC%81"

# WebAPI呼び出し
curl -X 'GET' \
  "http://localhost:8000/voice?text=${ENCODED_TEXT}&model_name=${MODEL_NAME}&speaker_id=${SPEAKER_ID}&sdp_ratio=0.2&noise=0.6&noisew=0.8&length=1&language=JP&auto_split=true&split_interval=0.5&assist_text_weight=1&style=Neutral&style_weight=1" \
  -H 'accept: audio/wav' --output output.wav

# output.wav に合成された音声が格納される
```
