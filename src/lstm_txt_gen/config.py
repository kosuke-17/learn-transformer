import os

DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
# コーパスとは、機械学習や自然言語処理などのタスクに利用する、大量のテキストデータの集まり
DIR_CORPUS = os.path.join(DIR_ROOT, "corpus")
DIR_MODEL = os.path.join(DIR_ROOT, "model")

FILE_AOZORA_ZIP = os.path.join(DIR_CORPUS, "aozora.zip")

FILE_CORPUS_TXT = os.path.join(DIR_CORPUS, "corpus.txt")
