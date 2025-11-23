import torch
from config import *
import utils
from model_transformer import *

# トークン辞書を読み込む
utils.id2token = utils.load_json(FILE_ID2TOKEN)
utils.token2id = utils.load_json(FILE_TOKEN2ID)
vocab_size = len(utils.token2id)

# モデルをインスタンス化して、保存済みのモデルを読み込む
model = TransformerModel(vocab_size, EMBED_DIM, NUM_HEADS, NUM_LAYERS)
model.load_state_dict(torch.load(FILE_MODEL))
model.to(device)
model.eval() # 推論モデルに変更

def generate(start_text, max_length=100, temperature=1.0):
    """モデルを使って文章を作成する"""
    # トークンIDに変換
    start_token = text_to_ids(start_text, add_new=True)
    if any(token == UNK for token in start_token):
        print(f"未知語が含まれています: {start_text}")
    input_ids = [SOS] + start_token
    result = input_ids.copy()

    # 生成ループ
    for _ in range(max_length - 2):
        # バッチサイズのテンソルに変換
        input_ids = result[-SEQ_LENGTH:] # 最新のSEQ_LENGTH個のトークンを取得
        input_tensor = torch.tensor(input_ids).unsqueeze(0).to(device)
        with torch.no_grad():
            # モデルに入力
            logits = model(input_tensor)
            logits = logits[0, -1, :] / temperature
            # ソフトマックス関数で確率に変換
            probs = torch.softmax(logits, dim=-1)
            # 確率分布からトークンIDをサンプリング
            next_id = torch.multinomial(probs, num_samples=1).item()
            if next_id == EOS: # EOSトークンが出たら終了
                break
            result.append(next_id) # 結果に追加
    # テキストに変換して、返す
    return utils.ids_to_text(result, skip_special=True)

if __name__ == "__main__":
    for _ in range(3): # 3回繰り返す
        text = generate("システムで大切なのは")
        print("-", text)
        text = generate("アイデアは")
        print("-", text)
        text = generate("")
        print("-", text)

