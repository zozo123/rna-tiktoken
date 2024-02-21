import argparse
import json
import pandas as pd
from collections import Counter
from tokenizers import Tokenizer, trainers, models, decoders


class RNATikTokComplete:
    def __init__(self, tokenization_strategy="kmer", k=3, bpe_merges=1000):
        self.k = k
        self.vocab = Counter()
        self.strategy = tokenization_strategy
        self.bpe_merges = bpe_merges

        if self.strategy == "bpe":
            self.tokenizer = Tokenizer(models.BPE())
            self.tokenizer.decoder = decoders.BPEDecoder()

    def fit(self, sequences):
        if self.strategy == "bpe":
            trainer = trainers.BpeTrainer(
                vocab_size=self.bpe_merges,
                min_frequency=1,
                special_tokens=["<pad>", "<unk>", "<s>", "</s>", "<mask>"],
            )
            self.tokenizer.train_from_iterator(sequences, trainer)
        else:
            for seq in sequences:
                tokens = self._tokenize_sequence(seq)
                for token in tokens:
                    self.vocab[token] += 1

    def _bpe_tokenize(self, sequence):
        encoding = self.tokenizer.encode(sequence)
        return encoding.tokens

    def _kmer_tokenize(self, sequence):
        tokens = []
        for i in range(len(sequence) - self.k + 1):
            kmer = sequence[i : i + self.k]
            tokens.append(kmer)
        return tokens

    def _tokenize_sequence(self, sequence):
        if self.strategy == "kmer":
            return self._kmer_tokenize(sequence)
        elif self.strategy == "bpe":
            return self._bpe_tokenize(sequence)

    def tokenize(self, sequence):
        tokens = self._tokenize_sequence(sequence)
        if self.strategy == "kmer":
            return [token for token in tokens if token in self.vocab]
        else:
            return tokens

    def get_vocabulary(self):
        if self.strategy == "kmer":
            return self.vocab
        elif self.strategy == "bpe":
            return self.tokenizer.get_vocab()


def test_RNATikTokComplete():
    tokenizer = RNATikTokComplete(tokenization_strategy="bpe")
    training_sequences = [
        "ACGUACGU",
        "UGCAUGCAAGGCUUAGCUAG",
        "CGUACGUAC",
        "AUCGAUCG",
        "AUCG",
    ]
    tokenizer.fit(training_sequences)
    sequence = "ACGUACGUAUCG"
    tokens = tokenizer.tokenize(sequence)
    assert len(tokens) > 0, "Tokenization failed"
    print("Test passed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a tokenizer on RNA sequences.")
    parser.add_argument(
        "--strategy",
        type=str,
        default="bpe",
        help='Tokenization strategy to use. Options are "bpe" or "kmer".',
    )
    parser.add_argument(
        "--k", type=int, default=3, help="Size of k for kmer tokenization."
    )
    parser.add_argument(
        "--bpe_merges", type=int, default=1000, help="Number of BPE merges to perform."
    )
    args = parser.parse_args()

    tokenizer = RNATikTokComplete(
        tokenization_strategy=args.strategy, k=args.k, bpe_merges=args.bpe_merges
    )
    df_train = pd.read_csv("./test_sequences.csv")
    df_train = df_train[["sequence"]]
    df_rna_central = pd.read_csv("./rna_central_sequences.csv")
    df_rna_central = df_rna_central.drop(columns=["len"])
    df_train = df_train.append(df_rna_central)
    df_train = df_train.drop_duplicates()
    sequences = df_train["sequence"].tolist()
    tokenizer.fit(sequences)

    vocab = tokenizer.get_vocabulary()
    print(len(vocab))

    with open("./vocab_test_seqeunces_all.json", "w") as f:
        json.dump(vocab, f)

    test_RNATikTokComplete()
