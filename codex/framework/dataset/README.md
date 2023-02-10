### Dataset (assertion generation)
Dataset for assertion generation:

```
atlas-dataset
├── Eval
│             ├── assertLines.txt
│             └── testMethods.txt
├── Testing
│             ├── assertLines.txt
│             └── testMethods.txt
└── Training
    ├── assertLines.txt
    └── testMethods.txt.zip
```

### Dataset (program repair)
Dataset for program repair:
```
tfix-dataset
└── clean-test
    ├── test_data.json
    └── train_data.json
```

It should be noted that we have to compress large files before uploading them to GitHub. Before running the code, please uncompress these files.

### Dataset acknowledgements
We use the [ATLAS](https://arxiv.org/abs/2002.05800), and [TFix](https://proceedings.mlr.press/v139/berabi21a.html) dataset for our experiments. For the sake of simplicity, we have included the dataset in the repository. However, we would like to acknowledge the authors for making the dataset publicly available. 
