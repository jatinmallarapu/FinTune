# Design

Use a held-out rule-family split and a fixed five-label taxonomy. Stratifying individual rows would risk lexical leakage. Save the canonical hash with the split and compare all models on the same examples.

The local input and output contract is documented in the project README. The cloud integration and its API contract are separate milestones.
