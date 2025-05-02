# Python 3.11の公式イメージをベースに使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# プロジェクトファイルをコピー
COPY pyproject.toml ./

# uvをインストール
RUN pip install uv

# 仮想環境を作成してアクティベート
RUN uv venv
ENV PATH="/app/.venv/bin:$PATH"

# 依存関係をインストール
ARG STYLE_BERT_VITS2_DIR_NAME=Style-Bert-VITS2
RUN uv pip install "torch<2.4" "torchaudio<2.4" --index-url https://download.pytorch.org/whl/cu118

# setup requirements
COPY ${STYLE_BERT_VITS2_DIR_NAME}/requirements.txt ${STYLE_BERT_VITS2_DIR_NAME}/requirements.txt
RUN uv pip install -r ${STYLE_BERT_VITS2_DIR_NAME}/requirements.txt

# setup modules
COPY ${STYLE_BERT_VITS2_DIR_NAME} ${STYLE_BERT_VITS2_DIR_NAME}
ENV PYTHONPATH="/app/${STYLE_BERT_VITS2_DIR_NAME}"
WORKDIR /app/${STYLE_BERT_VITS2_DIR_NAME}

# download models
COPY model_downloader model_downloader
RUN python model_downloader/initialize_1.py
RUN python model_downloader/initialize_2.py
RUN python model_downloader/initialize_3.py
RUN python model_downloader/initialize_4.py
RUN python model_downloader/initialize_5.py
RUN python model_downloader/initialize_6.py


# アプリケーションコードをコピー
# COPY . .

RUN mkdir -p /app/${STYLE_BERT_VITS2_DIR_NAME}/static
# WORKDIR /app/${STYLE_BERT_VITS2_DIR_NAME}
# RUN python initialize.py  # 必要なモデルとデフォルトTTSモデルをダウンロード

# 必要に応じて制限を変更してください
#CMD ["python", "server_editor.py", "--line_length", "50", "--line_count", "3", "--skip_static_files"]
CMD ["python", "server_fastapi.py"]
# # コンテナ起動時のコマンドを設定
# CMD ["python", "-m", "emotional_text_to_speech"] 