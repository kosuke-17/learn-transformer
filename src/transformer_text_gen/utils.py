from janome.tokenizer import Tokenizer

tokenizer = Tokenizer()

# 特殊トークンを定義
UNK = 0 # 未知語
SOS = 1 # 文の開始
EOS = 2 # 文の終了
PAD = 3 # パディング


token2id = {
    "<UNK>": UNK,
    "<SOS>": SOS,
    "<EOS>": EOS,
    "<PAD>": PAD,
}
id2token = {
    "0": "<UNK>",
    "1": "<SOS>",
    "2": "<EOS>",
    "3": "<PAD>",
}

# 例

def token_to_id(text, add_new=False):
    """
    テキスト（トークン）を対応するIDに変換する関数
    
    この関数は、与えられたテキスト（単一のトークン）を辞書（token2id）に基づいて
    数値IDに変換します。未知語（辞書に存在しないトークン）の処理方法を
    add_newパラメータで制御できます。
    
    Args:
        text (str): 変換したいテキスト（トークン）
        add_new (bool): 未知語を新規追加するかどうか
            - False: 未知語の場合は<UNK>のID（0）を返す（デフォルト）
            - True: 未知語の場合は新しいIDを割り当てて辞書に追加する
    
    Returns:
        int: テキストに対応するID
    
    Examples:
        # 既知のトークンの場合
        >>> text_to_ids("<SOS>")
        1
        
        >>> text_to_ids("<EOS>")
        2
        
        # 未知語でadd_new=Falseの場合（デフォルト）
        >>> text_to_ids("hello")
        0  # <UNK>のIDを返す
        
        # 未知語でadd_new=Trueの場合
        >>> text_to_ids("world", add_new=True)
        4  # 新しいIDを割り当てて返す（既存のIDが0-3まであるため）
        
        # その後、同じトークンは追加されたIDを返す
        >>> text_to_ids("world")
        4
    """
    if text not in token2id:
        if not add_new:
            return token2id["<UNK>"]
        new_id = len(token2id)
        token2id[text] = new_id
        id2token[str(new_id)] = text
    return token2id[text]

def text_to_ids(text, add_new=False):
    """テキストをIDに変換する"""
    ids = []
    for token in tokenizer.tokenize(text):
        token_id = token_to_id(token.surface, add_new)
        ids.append(token_id)
    return ids

def save_json(data, file_path):
    """データをJSON形式で保存する"""
    import json
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def load_json(file_path):
    """JSON形式で保存されたデータを読み込む"""
    import json
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)