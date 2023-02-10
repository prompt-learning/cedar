import lizard
from transformers import GPT2TokenizerFast

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def count_codex_tokens(input: str):
    """
    word count does not equate to token count for gpt models.
    So we need to get token count for a string using the gpt tokenizers.
    https://beta.openai.com/tokenizer
    """
    res = tokenizer(input)['input_ids']
    return len(res)


def completions_create_tokens(prompt: str, max_tokens: int, n: int = 1) -> int:
    """
    Returns the upper bound of total tokens consumed for a completions.create() request.

    The formula is

      prompt_tokens + n * max_tokens

    Note that completions can be shorter than max_tokens if a sample produces a stop sequence. In this case the total tokens are lower than the above estimate.
    """
    prompt_tokens = tokenizer.encode(prompt)
    return len(prompt_tokens) + n * max_tokens


def engines_generate_tokens(context: str, length: int, completions: int = 1) -> int:
    """
    Code taken from https://replit.com/@NikolasTezak/API-TokenLoadEstimator#main.py
    Returns the upper bound of total tokens consumed for a engines.generate() request.

    This is an older but equivalent API call to completions.create(), see above.

    here max_tokens is in the in predictions response
    """
    return completions_create_tokens(
        prompt=context,
        max_tokens=length,
        n=completions,
    )


def word_count(query):
    """count the number of words in a string"""
    return len(query.split())

def complexity_count(code: str) -> str:
    i = lizard.analyze_file.analyze_source_code("./test.java", code)

    complexity = i.average_cyclomatic_complexity
    complexity_type = ''
    if complexity >= 1 and complexity <= 10:
        complexity_type = 'simple'
    elif complexity >= 11 and complexity <= 20:
        complexity_type = 'complex'
    elif complexity >= 21 and complexity <= 50:
        complexity_type = 'too complex'

    return complexity_type

if __name__ == "__main__":
    print(count_codex_tokens("Hello world vancouver"))
    print(engines_generate_tokens("Hello world vancouver", length=1000, completions=1))
