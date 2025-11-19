"""青空文庫の全テキストをダウンロードして解凍するスクリプト"""
import os
import requests
import zipfile
from config import *

url = "https://github.com/aozorahack/aozorabunko_text/archive/refs/heads/master.zip"

if not os.path.exists(DIR_CORPUS):
    os.makedirs(DIR_CORPUS)
if not os.path.exists(DIR_MODEL):
    os.makedirs(DIR_MODEL)

if not os.path.exists(FILE_AOZORA_ZIP):
    # withブロックを抜けると自動的にリソースが解放
    # close()を書く必要がない
    # try catchはエラーハンドリングを目的としてる。
    # with文はリソース管理をしていて、ファイルやネットワーク接続などのクリーンアップを自動で行ってくれる。
    # 全文テキストはZIP解凍しても264MBもあるのでstream
    with requests.get(url, stream=True) as r:
        r.raise_for_status() # 問題があれば例外を発生
        print("ダウンロード中...", url)
        # バイナリモードでファイルを書き込む
        # バイナリモードはバイト単位でデータを読み書きするためのモード
        with open(FILE_AOZORA_ZIP, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024*8):
                f.write(chunk)
                print(".", end="", flush=True) # 1Bごとに進捗表示
            print("\nダウンロードが完了しました")
with zipfile.ZipFile(FILE_AOZORA_ZIP) as z:
    z.extractall(DIR_CORPUS)
    print("解凍が完了しました")