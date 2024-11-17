# Cam Hack 24

## To setup
```sh
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

## Setup API key
1. Install requirements: ```pip install -r requirements.txt```
2. Create an account and setup API key here: https://console.groq.com/keys
3. Create a file named `secrets.yaml`
4. Write in the file:
   ```
   groq:
     api_key: {YOUR_API_KEY}
   ```