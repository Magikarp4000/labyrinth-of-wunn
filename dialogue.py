import yaml
from groq import Groq

class Dialogue:
    def __init__(self):
        with open('secrets.yaml') as file:
            f = yaml.safe_load(file)
            self.key = f['groq']['api_key']
        self.client = Groq(api_key=self.key)

        get_background = self.client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": '''You are an NPC in a game with the following context:
                You are living in a big city.
                In your city, you have the following available locations: 'shop', 'cafe', 'haunted house', 'office' and 'cinema'.
                Generate a personality for the NPC.
                '''
            },
            {
                "role": "user",
                "content": '''Print 3 short sentences of around 10 words, that will be passed on as input to another LLM, that describes the personality of the character.
                Just print the 3 phrases; don't print anything else.'''
            }],
            model="llama-3.1-8b-instant",
            temperature=1.25,
            max_tokens=2048,
            top_p=1,
            stop=None,
            stream=False,
        )

        player_background = get_background.choices[0].message.content

        self.memory = [
                {
                    "role": "system",
                    'content': "Your personality can be described as follows: " + player_background +
                    '''You are living in a big city with a murderer on the run.
                    In your city, you have the following available locations: 'shop', 'cafe', 'office', 'alleyways' and 'cinema'.
                    You need to answer in JSON format. Make sure every reply is one sentence or so, as if in a realistic conversation. The average 
                    friendliness value is 50.
                    The JSON schema should include
{
  "action": {
    "location": "string (null, shop, office, haunted house, cinema, cafe)",
    "type": "string (null, walk, run, scream, suicide)",
    "friendliness": "integer (0 to 100)"
  },
  "dialogue": "string"
}'''
                },
        ]

    def test(self, prompt = None):
        if prompt == None:
            prompt = input()
        self.memory.append({
                "role": "user",
                "content": prompt,
        })
        chat_completion = self.client.chat.completions.create(
            messages=self.memory,
            model="llama-3.1-8b-instant",
            temperature=1.0,
            max_tokens=2048,
            top_p=1,
            stop=None,
            stream=False,
            response_format={"type": "json_object"}
        )
        x = chat_completion.choices[0].message.content
        self.memory.append({
            'role': 'assistant',
            'content': x
        })
        return x

if __name__ == '__main__':
    d = Dialogue()
    while True:
        print(d.test())
