from g4f.client import Client

# Initialize the client
client = Client()

# Define the messages for the chat
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Can you explain how to use the g4f library in Python?"}
]

# Create a streamed completion
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=1000,
    stream=True
)

# Collect and print the streamed response
output = ""
for completion in response:
    try:
        output += completion.choices[0].delta.content or ""
    except AttributeError:
        pass

print("Response:", output)
