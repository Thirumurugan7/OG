from freeGPT import Client

while True:
    prompt = input("👦: ")
    try:
        resp = Client.create_completion("gpt3_5", prompt)
        print(f"🤖: {resp}")
    except Exception as e:
        print(f"🤖: {e}")