### Setup environment for framework

```
# The following steps create an isolated environment codex-env and install required dependencies.

conda create --name codex-env python=3.9 # creates the codex-env environment
conda activate codex-env                 # activates the codex-env environment
conda install openai                     # installs dependency - openai

pip install backoff
pip install edit_distance
conda install difflib
conda install matplotlib
conda install plotly
conda install scipy
conda install sklearn

pip install tenacity
pip install suffix-trees
pip install lizard
conda install gensim
pip install rank_bm25
```

### Setup environment for embedding search 

We use [sentence-transformers](https://huggingface.co/flax-sentence-embeddings/st-codesearch-distilroberta-base) to generate embeddings for the code snippets.

```
conda create -n semantic-embedding --file embedding-prereq.txt
conda install -c pytorch faiss-cpu # install faiss-cpu
```

To install sentence-transformers, please follow the instructions from [here](https://huggingface.co/flax-sentence-embeddings/st-codesearch-distilroberta-base).
For linux environment, as stated in the above link, sentence-transformers gets installed using the following command: `pip install -U sentence-transformers`.

However, for mac with m1 chip, we had to run the following commands to get it installed:

```
conda list openmp
conda unistall intel-openmp
conda install -c conda-forge sentence-transformers
```

#### Install vector database
We use vector database lite for vector search. vdblite library details could be found [here](https://pypi.org/project/vdblite/).

```
pip install vdblite
```

### Generate embeddings for the code snippets
Run the following command to generate embeddings for ATLAS.

```
python atlas_generate_embedding.py
```

Run the following command to generate embeddings for TFix.

```
python tfix_generate_embedding.py
```

### Running evaluation
Results from experiments are saved in the folder `./codex/framework/result-analysis/final-results/`.
 
```
python evaluation/result_analysis_atlas.py ./results.csv
exact_match_count: 9021 match_count: 10368
exact match_count (%): 47.946, match_count(%): 55.105
```

### Dataset acknowledgements
We use the [ATLAS](https://arxiv.org/abs/2002.05800), and [TFix](https://proceedings.mlr.press/v139/berabi21a.html) dataset for our experiments. For the sake of simplicity, we have included the dataset in the repository. However, we would like to acknowledge the authors for making the dataset publicly available. 

