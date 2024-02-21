from collections import Counter


class RNATikTok:
    def __init__(self, k=3):
        self.k = k
        self.vocab = Counter()

    def fit(self, sequences):
        """Build the vocabulary based on a list of RNA sequences.

        :param sequences: List of RNA sequences to build the vocabulary from.
        """
        for seq in sequences:
            for i in range(len(seq) - self.k + 1):
                kmer = seq[i : i + self.k]
                self.vocab[kmer] += 1

    def tokenize(self, sequence):
        """Tokenize a given RNA sequence using the established vocabulary.

        :param sequence: RNA sequence to be tokenized.
        :return: List of tokens.
        """
        tokens = []
        i = 0
        while i < len(sequence):
            found = False
            for k in range(self.k, 0, -1):
                kmer = sequence[i : i + k]
                if kmer in self.vocab:
                    tokens.append(kmer)
                    i += k
                    found = True
                    break
            if not found:
                tokens.append(sequence[i])
                i += 1
        return tokens

    def get_vocabulary(self):
        """Return the established vocabulary.

        :return: Vocabulary as a Counter object.
        """
        return self.vocab


# Usage Example:

if __name__ == "__main__":
    # Initialize the tokenizer
    tokenizer = RNATikTok(k=3)

    # Fit the tokenizer on training RNA sequences
    training_sequences = ["ACGUACGU", "UGCAUGCA", "CGUACGUAC", "AUCGAUCG"]
    tokenizer.fit(training_sequences)

    # Tokenize a new sequence
    sequence = "ACGUACGUAUCG"
    tokens = tokenizer.tokenize(sequence)
    print("Tokenized Sequence:", tokens)

    # Get the established vocabulary
    vocab = tokenizer.get_vocabulary()
    print("Vocabulary:", vocab)
