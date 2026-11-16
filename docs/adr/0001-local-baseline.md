# Split by rule family

Sentence-level splits can leak near-duplicate clauses. Assigning rule families as groups keeps each family in one partition. Small corpora can have unbalanced classes or empty partitions, so check label and family counts before training.
