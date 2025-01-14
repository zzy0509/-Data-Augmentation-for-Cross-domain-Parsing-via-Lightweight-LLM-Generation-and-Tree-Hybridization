# Data-Augmentation-for-Cross-domain-Parsing-via-Lightweight-LLM-Generation-and-Tree-Hybridization

Code for Coling-2025's paper Data Augmentation for Cross-domain Parsing via Lightweight LLM Generation and Tree Hybridization

## Requirements:

- nltk: >= 3.4.5
- transformers: >= 2.1.1

## Preparation

- In-domain dataset, e.g., PTB
- Cross-domain dataset, e.g., MCTB
- Large-scale target-domain raw texts
- Get [Berkeley Neural Parser](https://github.com/nikitakit/self-attentive-parser)
  ```
  cd /LLM_Tree_Hybridization/
  git clone https://github.com/nikitakit/self-attentive-parser.git
   ```

## Usage

### Generating Target-Domain Subtrees via LLM

1. Extracting Domain Dictionary and Lexicalized Grammar Rules.

   ```
   LLM_Tree_Hybridization/LLM_generation/prepocess
   ```

   

2. LLM Prompting with Target-domain Words and Lexicalized Grammar Rules.

   ```
   LLM_Tree_Hybridization/LLM_generation/LLM
   ```

   

### Tree Hybridization

Try the following commands to make the hybridization.

```
sh LLM_Tree_Hybridization/Tree_hybridization/hybrid.sh
```

