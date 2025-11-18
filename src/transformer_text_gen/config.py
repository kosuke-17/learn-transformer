"""プロジェクト全体の設定をまとめる"""
import os

DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
# コーパスとは言語データの集積を指す言葉
# absolute pathは絶対パスを返す
CORPUS_DIR = os.path.abspath(os.path.join(DIR_ROOT, "corpus"))
# コーパスの最大行数
CORPUS_MAX_LINES = 20000

DIR_MODEL = os.path.join(DIR_ROOT, "model")

DIR_CORPUS_SOURCE= os.path.abspath(os.path.join(DIR_ROOT, "..", "kinokobooks"))

FILE_CORPUS = os.path.join(CORPUS_DIR, "corpus.txt")
FILE_MODEL = os.path.join(DIR_MODEL, "model_transformer.path") 

# データセットの保存先
FILE_IDS = os.path.join(DIR_MODEL, "ids.json")
FILE_TOKEN2ID = os.path.join(DIR_MODEL, "token2id.json")
FILE_ID2TOKEN = os.path.join(DIR_MODEL, "id2token.json")

# ハイパーパラメータ
EMBED_DIM = 512
NUM_HEADS = 8
NUM_LAYERS = 4
BATCH_SIZE = 64
SEQ_LENGTH = 50 # シーケンスの最大長
OPTIMIZER_LR=1e-5 # 最適化アルゴリズムの学習率
EPOCHS=500

EARLY_STOPPING_LOSS = 1.8