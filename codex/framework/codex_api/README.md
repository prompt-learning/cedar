### OpenAI Codex API
Before running teh code you need to set the OpenAI API key. You can get the key following steps [here](https://beta.openai.com/docs/api-reference/authentication). 

In the code, we set API keys (`OPENAI_API_KEYS` array) using the following code snippet in codex_api.py:

```
OPEN_API_KEY=<your-key>
OPENAI_API_KEYS = [
    os.getenv("OPENAI_API_KEY")
]
``` 

If you have multiple API keys, you can set them as follows:

```
OPEN_API_KEY=<your-key>
OPENAI_API_KEY_1=<your-key-1>
OPENAI_API_KEY_2=<your-key-2>

Then update the code in codex_api.py as follows:

OPENAI_API_KEYS = [
    os.getenv("OPENAI_API_KEY"),
    os.getenv("OPENAI_API_KEY_1"),
    os.getenv("OPENAI_API_KEY_2")
]
```

The rest of the code will automatically use the API keys in a round-robin fashion.