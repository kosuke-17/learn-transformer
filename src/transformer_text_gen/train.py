from datetime import datetime
from config import *
# ディープラーニングモデルを構築、トレーニング、評価するための強力なライブラリ
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from model_transformer import TransformerModel, device
import utils

utils.id2token = utils.load_json(FILE_ID2TOKEN)
utils.token2id = utils.load_json(FILE_TOKEN2ID)
vocab_size = len(utils.token2id)
ids = utils.load_json(FILE_IDS)

# データセットを定義
class TokenDataset(Dataset):
    """トークンデータセット"""
    def __init__(self, data):
        """初期化"""
        items = []
        # データ長をSEQ_LENGTHと揃える
        for tokens in data:
            if len(tokens) < SEQ_LENGTH:
                # トークン数がSEQ_LENGTH未満の場合はパディングを追加
                tokens = utils.pad_sequence(tokens, SEQ_LENGTH)
            # トークン数がSEQ_LENGTHより多い場合は切り詰める
            tokens = tokens[:SEQ_LENGTH]
            # トークンをテンソルに変換
            # torch.Tensorは、単一のデータ型を持つ要素を含む多次元行列
            # https://docs.pytorch.org/docs/stable/tensors.html
            items.append(torch.tensor(tokens))
        self.data = items

    def __len__(self):
        """データセットの長さを返す"""
        return len(self.data)

    def __getitem__(self, index):
        """
        データセットの要素を返す
        
        このメソッドは、箱（データセット）から指定された番号のデータを取り出して、
        機械学習で使える形に変換します。
        
        具体例：
        元のデータ: [1, 10, 11, 12, 13, 14, 15]
        （これは「こんにちは、元気ですか」という文を数字に変換したもの）
        
        x（入力データ）: [1, 10, 11, 12, 13, 14]
        → 最後の1つを除いた部分。これが「問題」になります。
        
        y（正解データ）: [10, 11, 12, 13, 14, 15]
        → 最初の1つを除いた部分。これが「答え」になります。
        
        なぜ1つずらすの？
        機械学習モデルに「前の文字を見て、次の文字を予測する」練習をさせるためです。
        例えば：
        - x = 「こんにちは、元気で」
        - y = 「こんにちは、元気です」
        モデルは「で」の次が「す」だと学習します。
        """
        # 箱から指定された番号（index）のデータを取り出す
        # 例：index=0 なら1番目のデータ、index=1 なら2番目のデータ
        tokens = self.data[index]
        
        # 入力データ（x）：最後の1つを除いた部分
        # 例：[1, 10, 11, 12, 13, 14, 15] → [1, 10, 11, 12, 13, 14]
        # これは「問題」として使います
        x = tokens[:-1]
        
        # 正解データ（y）：最初の1つを除いた部分
        # 例：[1, 10, 11, 12, 13, 14, 15] → [10, 11, 12, 13, 14, 15]
        # これは「答え」として使います
        y = tokens[1:]
        
        # x（問題）とy（答え）の2つを返す
        return x, y

def check_xy(x, y):
    """xとyのトークンを表示する"""
    text_x = utils.ids_to_text(x.tolist(), skip_special=False, split_mark="|")
    text_y = utils.ids_to_text(y.tolist(), skip_special=False, split_mark="|")
    print(f" x: {text_x.replace('<PAD>', '')}")
    print(f" y: {text_y.replace('<PAD>', '')}")

model = TransformerModel(vocab_size, EMBED_DIM, NUM_HEADS, NUM_LAYERS).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=OPTIMIZER_LR)
criterion = nn.CrossEntropyLoss(ignore_index=utils.PAD)
dataset = TokenDataset(ids)
loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# 学習ループ
loss_history = []
loss_val = 0
for epoch in range(EPOCHS):
    # 学習データを読み出して学習
    data_size = len(loader)
    for i, (x, y) in enumerate(loader):
        x, y = x.to(device), y.to(device)
        logits = model(x) # モデルに入力
        loss = criterion(logits.view(-1, vocab_size), y.view(-1)) # 損失計算
        optimizer.zero_grad() # 勾配を初期化
        loss.backward() # 勾配を計算
        optimizer.step() # 重み更新
        loss_val = loss.item() # 損失値を取得
        if i % 50 == 0:
            per = int(i / data_size * 100)
            print(f" - {i:3}/{data_size} ({per:2}%), Loss: {loss_val:.4f}")
            check_xy(x[0], y[0])
    # 学習データの損失値を履歴に記録
    history = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "epoch": epoch + 1,
        "loss": loss_val,
        "saved": False,
    }
    # 学習経過の調査のために、定期的にモデルを保存
    if epoch % 10 == 9:
        history["saved"] = True
        torch.save(model.state_dict(), FILE_MODEL + f"_{epoch + 1}.pt")
    loss_history.append(history)
    print(f"* Epoch: {epoch + 1:03}/{EPOCHS}, Loss: {loss_val:.4f}")
    if loss_val < EARLY_STOPPING_LOSS:
        print(f"Early stopping at epoch {epoch + 1}, loss:")
        break

torch.save(model.state_dict(), FILE_MODEL)
utils.save_json(loss_history, FILE_MODEL + "_history.json")
print("モデルを保存しました")