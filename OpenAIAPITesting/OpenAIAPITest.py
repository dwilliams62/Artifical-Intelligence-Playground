from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Is ChatGPT 4o mini good for classifying documents based off predetermined rules and adding a label to the document accordingly?"
        }
    ]
)

print(completion.choices[0].message)