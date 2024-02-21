# RNA TikTokComplete (extracted and rewritten from a different research project, TBD make sure it has all components.)

RNA TikTokComplete is a Python library for tokenizing RNA sequences. It's designed for bioinformatics researchers and developers who work with RNA sequence data. It supports two tokenization strategies: "kmer" and "bpe" (Byte Encoding).

## Installation

You can install the required dependencies with pip:

pip install -r reqs.txt

## Usage

Here's a basic example of how to use RNA TikTokComplete:

```
from RNATikTokComplete import RNATikTokComplete

tokenizer = RNATikTokComplete(tokenization_strategy="bpe")
sequence = "AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA"
tokens = tokenizer.tokenize(sequence)

print(tokens)
```

## API Reference

The main class in RNA TikTokComplete is the `RNATikTokComplete` class, which has the following methods:

- fit(sequences: List[str]): Trains the tokenizer on a list of RNA sequences.
- tokenize(sequence: str) -> List[str]: Tokenizes an RNA sequence into a list of tokens.
- get_vocabulary() -> Union[Counter, Dict[str, int]]: Returns the vocabulary that the tokenizer has learned. The type of the returned value depends on the tokenization strategy.

## Tests

You can run the tests for RNA TikTokComplete with:

`python RNATikTokComplete.py`
