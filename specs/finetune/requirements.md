# Regulatory obligation classification

An analyst needs to distinguish obligations, prohibitions, permissions, definitions and other statements.

| ID | Requirement | Acceptance criterion |
| --- | --- | --- |
| REQ-01 | Group isolation | GIVEN multiple sentences from a rule family WHEN splitting data THEN keep that family in a single partition. |
| REQ-02 | Data validation | GIVEN duplicate example IDs or unknown labels WHEN loading THEN reject the dataset. |
| REQ-03 | Scoring | GIVEN predictions for a labelled set WHEN scoring THEN report accuracy, macro F1 and exact confusion counts. |
| REQ-04 | Missing prediction handling | GIVEN an invalid model label WHEN scoring THEN count it as an error rather than dropping it. |
