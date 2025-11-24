import os

# 正規表現のためにインポート
# https://docs.python.org/ja/3/library/re.html
import re

from config import CORPUS_DIR, DIR_CORPUS_SOURCE, DIR_MODEL, FILE_CORPUS

# コーパスとモデルのフォルダを作成

lines = []

os.makedirs(CORPUS_DIR, exist_ok=True)
os.makedirs(DIR_MODEL, exist_ok=True)

for root, dirs, files in os.walk(DIR_CORPUS_SOURCE):
    for fname in files:
        # 拡張子を調べて、"*.mdのみ"を対象にする
        if not fname.endswith(".md") or fname == "README.md":
            continue
        print(f"{fname}を処理中...")
        file_path = os.path.join(root, fname)
        # with文を使ってファイルを開く
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            # マークダウンのコードブロックを削除
            text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
            text = text.replace("。", "。\n")  # 改行を追加
            text = text.replace("?", "?\n")  # 改行を追加
            text = text.replace("!", "!\n")  # 改行を追加
            text = re.sub("\*\*|　", "", text)  # 太字を削除
            text = re.sub(r"(\(.+?\)|（.+?）)", "", text)  # ()を削除
            text = re.sub(r"\[.+?\]", "", text)  # []を削除
            text = re.sub(
                r"(https?|mailto)\:[a-zA-Z0-9~_/@\-\.\?]+", "", text
            )  # URLを削除
            # 一行ずつ処理
            for line in text.splitlines():
                # 文字列の両端にある空白を取り除く
                line = line.strip()
                if line == "":
                    continue
                # 行の先頭を確認して、コーパスに含めないようにする（ヘッダーなど）
                if line[0] in "#-*|><":
                    continue
                lines.append(line)
# 文字列を改行で結合して、ファイルに書き込む
text = "\n".join(lines)
with open(FILE_CORPUS, "w", encoding="utf-8") as f:
    f.write(text)
print(f"コーパスの作成が完了しました。 {len(lines)}行のデータが作成されました。")
