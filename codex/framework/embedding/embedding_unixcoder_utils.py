import torch

from unixcoder import UniXcoder

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = UniXcoder("microsoft/unixcoder-base")
model.to(device)


def get_unixcoder_embedding(code: str):
    func = code
    tokens_ids = model.tokenize([func], max_length=4096, mode="<encoder-only>")
    source_ids = torch.tensor(tokens_ids).to(device)
    tokens_embeddings, max_func_embedding = model(source_ids)

    # replace newlines, which can negatively affect performance.
    # code = code.replace("\n", " ")
    return max_func_embedding
