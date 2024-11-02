import yaml
from groq import Groq

class Dialogue:
    def __init__(self):
        with open('secrets.yaml') as file:
            f = yaml.safe_load(file)
            self.key = f['groq']['api_key']
        self.client = Groq(api_key=self.key)

        self.memory = [
                {
                    "role": "system",
                    "content": "You are living in a big city with murders on the run. In your city, you have the following available locations: 'shop', 'cafe', 'police office', 'office', 'alleyways' and 'cinema'. You are a 30 year old man. Make sure every reply is one sentence or so, as if in a realistic conversation. Scream if you feel unsafe of your own situation e.g. if you think you are about to be robbed or killed. If you're screaming, say SCREAM in full caps, if you're running away, say RUN in full caps followed by where you want to go.",
                },
        ]

    def test(self):
        i = input()
        self.memory.append({
                "role": "user",
                "content": i,
        })
        chat_completion = self.client.chat.completions.create(
            messages=self.memory,
            model="llama-3.1-8b-instant",
            temperature=1.0,
            max_tokens=2048,
            top_p=1,
            stop=None,
            stream=False,
        )
        x = chat_completion.choices[0].message.content
        print(x)
        self.memory.append({
            'role': 'assistant',
            'content': x
        })

if __name__ == '__main__':
    d = Dialogue()
    while True:
        d.test()
