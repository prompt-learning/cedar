# Code Example Demonstration Automated Retrieval (CEDAR)

## Paper

[Retrieval-Based Prompt Selection for Code-Related Few-Shot Learning](https://people.ece.ubc.ca/amesbah/resources/papers/cedar-icse23.pdf), 
Published at IEEE/ACM International Conference on Software Engineering (ICSE), 2023.

## Setup environment
- Prerequisite:
  - Install [conda](https://docs.conda.io/projects/conda/en/4.6.1/user-guide/install/macos.html) package manager. 

- Create python environment with required dependencies (for example, `openai`). 

```
# The following steps create an isolated environment codex-env and install the required dependencies.

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

- We have to compress large files in order to upload them to GitHub.
  - Please uncompress these files before running the code.
  - For example, uncompress this [file](./codex/framework/dataset/atlas-dataset/Training/testMethods.txt.zip) before running the code.

### Setup environment for embedding search

We use [sentence-transformers](https://huggingface.co/flax-sentence-embeddings/st-codesearch-distilroberta-base) to generate embeddings for the code snippets. 

```
conda create -n semantic-embedding --file embedding-prereq.txt # create the semantic-embedding environment
conda install -c pytorch faiss-cpu # install faiss-cpu
```

To install `sentence-transformers`, please follow the instructions from [here](https://huggingface.co/flax-sentence-embeddings/st-codesearch-distilroberta-base). 
For linux environment, as stated in the above link, sentence-transformers gets installed using the following command: `pip install -U sentence-transformers`.

However, for mac with m1 chip, we had to run the following commands to get it installed:
```
conda list openmp
conda unistall intel-openmp
conda install -c conda-forge sentence-transformers
```

### Install vector database
We use vector database lite (like SQLITE but for vector search). vdblite library details could be found [here](https://pypi.org/project/vdblite/).  

```
pip install vdblite
```

## Running experiment

Set OpenAI key:
```
export OPENAI_API_KEY=<your-key> 
```

Run the following script, to run the experiments for `atlas`:
```
python main_atlas.py
```

Run the following script, to run the experiments for `tfix`:
```
python main_tfix.py
```

For all the different configurations, please use command line parameters accordingly. More details about the command line parameters could be found in the [main_atlas.py](./codex/framework/main_atlas.py) and [main_tfix.py](./codex/framework/main_tfix.py) files. Also, each folder contains a README file with more details.  

## Running evaluation

After running the experiments, results are saved in the folder: `./codex/framework/results/`.

Run the following script, to see the evaluation metrics.

```
python evaluation/result_analysis_atlas.py ./results.csv
```
