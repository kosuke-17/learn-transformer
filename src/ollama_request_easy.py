import requests

API_ENDPOINT = "http://localhost:11434"

def generate_response(prompt):
    url = f"{API_ENDPOINT}/api/generate"
    data = {
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False,
    }
    response = requests.post(url, json=data)

    if response.status_code == 200:
        data = response.json()
        return data["response"]
    else:
        raise Exception(f"呼び出し失敗: {response.status_code} \n{response.text}")

# ハルシネーションをしました😢
# 2022 FIFA W杯では、アメリカが優勝しました。
if __name__ == "__main__":
    print(generate_response("直近のサッカーW杯の優勝国はどこですか？"))