import random

from config import (
    CORPUS_MAX_LINES,
    FILE_CORPUS,
    FILE_ID2TOKEN,
    FILE_IDS,
    FILE_TOKEN2ID,
    SEQ_LENGTH,
)
from utils import EOS, SOS, id2token, save_json, text_to_ids, token2id


# 単語辞書とIDリストからなるデータセットを作成
def make_dataset():
    """データセットを作成"""
    result = []
    with open(FILE_CORPUS, "r", encoding="utf-8") as f:
        text = f.read()
        lines = text.splitlines()
        random.shuffle(lines)
        lines = lines[:CORPUS_MAX_LINES]  # コーパスの最大行数を超えないようにする
        for i, line in enumerate(lines):
            if i % 1000 == 0:
                print(f"{i}/{len(lines)}行を処理しました")
            line = line.strip()
            ids = text_to_ids(line, add_new=True)
            tokens = [SOS] + ids + [EOS]
            if len(tokens) < 7 or len(tokens) > SEQ_LENGTH:
                continue
            result.append(tokens)
    # データセットの保存
    save_json(result, FILE_IDS)
    # トークン辞書の保存
    save_json(token2id, FILE_TOKEN2ID)
    save_json(id2token, FILE_ID2TOKEN)
    print("データセットの作成が完了しました。 ")
    print(f"トークン数: {len(token2id)}")
    print(f"データ数: {len(result)}")


if __name__ == "__main__":
    make_dataset()
