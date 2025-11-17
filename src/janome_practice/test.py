from janome.tokenizer import Tokenizer

sample_text = "思考力があれば、どんなことでも解決できる。"

tokenizer = Tokenizer()

tokens = list(tokenizer.tokenize(sample_text))

surface_list = [token.surface for token in tokens]

print("|".join(surface_list))
print("--------")

for t in tokens:
    face = t.surface # 表層系
    pos = t.part_of_speech # 品詞
    base = t.base_form # 基本形
    reading = t.reading # 読み
    phonetic = t.phonetic # 発音
    print(f"{face}\t{pos}\t{base}\t{reading}\t{phonetic}")