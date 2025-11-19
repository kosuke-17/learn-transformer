"""青空文庫のテキストをすべて結合して1つのテキストファイルにする"""
import os
# 正規表現のため
import re
from config import *

authors = ["夏目漱石", "太宰治", "芥川竜之介", "宮沢賢治"]

def enum_files(path):
    """指定したディレクトリ内のすべてのテキストファイルを列挙する"""
    # 指定したディレクトリのファイルを再帰的に探索する
    # サブフォルダまで含む
    for root, dirs, files in os.walk(path):
        for file in files:
            # txtの拡張子ファイルのみを対象にする
            if file.endswith(".txt"):
                # ファイルのパスを返す
                yield os.path.join(root, file)

def make_corpus():
    """青空文庫のテキストをすべて結合して1つのテキストファイルにする"""
    with open(FILE_CORPUS_TXT, "w", encoding="utf-8") as outfile:
        for file in enum_files(DIR_CORPUS):
            try:
                # 青空文庫のテキストはShift_JIS(CP932)
                with open(file, "r", encoding="cp932") as infile:
                    text = format_text(infile.read())
                    if len(text) < 300:
                        continue
                    # 特定の作家の作品のみを抽出する
                    # 0文字目から300文字
                    sub_text = text[0:300]
                    found = None
                    for author in authors:
                        if author in sub_text:
                            found = author
                            break
                    if found is None:
                        continue
                    print("結合中:", found, os.path.basename(file))
                    outfile.write(text + "\n")
            except UnicodeDecodeError:
                print(f"エラー: {file}の読み込みに失敗")
                continue
        print("コーパスの作成が完了しました。")

def format_text(text):
    """青空文庫のテキストを整形する"""
    text = text.replace("\r\n", "\n") # 改行コードをLFに変換
    # テキスト中に現れる記号についてを削除
    blocks = re.split("-{10,}\n", text)
    if len(blocks) >= 3:
        text = blocks[0] + "\n" + blocks[2]
        text = text.strip()
    # 末尾の情報を削除
    blocks = re.split(r"\n底本[：:]", text)
    text = blocks[0]
    # ルビや注釈を削除
    text = re.sub(r"《.+?》", "", text)  # ルビを削除
    text = re.sub(r"［＃.+?］", "", text)  # 注釈を削除
    text = re.sub(r"^\s+", "", text, flags=re.MULTILINE)  # 行頭の空白を削除
    text = re.sub(r"\n+", "\n", text)  # 連続する改行を1つにまとめる
    text = re.sub(r"[｜|｜「」『』]", "", text)  # 記号を削除
    return text

if __name__ == "__main__":
    make_corpus()