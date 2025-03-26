from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)