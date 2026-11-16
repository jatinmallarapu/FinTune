# FinTune

[![CI](https://github.com/jatinmallarapu/FinTune/actions/workflows/ci.yml/badge.svg)](https://github.com/jatinmallarapu/FinTune/actions/workflows/ci.yml)

Classify regulatory obligations with a reproducible data split and a benchmark contract for future model runs.

## Architecture

```text
Labelled statements → rule-family grouping → deterministic baseline → confusion matrix and macro F1
```

## Verification

| Scope | What the tests cover |
| --- | --- |
| Local acceptance tests | Group isolation, data validation, macro F1, and invalid label handling |
| Keyword baseline on 10 synthetic rows | 70% accuracy and 0.727 macro F1 |
| Production benchmark | Pending |

The synthetic baseline misses implicit requirements and permissions, which identifies two cases to include in a reviewed evaluation set.

## Quickstart

Python 3.11 or newer.

```sh
python fintune.py baseline examples/synthetic.json
python -m pip install -e '.[dev]'
make test
```

## Design and data

The ten original synthetic sentences exercise five labels. Required actions are obligations, forbidden actions are prohibitions, allowed actions are permissions, explicit meanings are definitions, and background statements are other.

[Requirements](specs/finetune/requirements.md) · [Design](specs/finetune/design.md) · [Tasks](specs/finetune/tasks.md)

[Architecture decision](docs/adr/0001-local-baseline.md)

## Remaining milestones

Reviewed dataset, QLoRA, SageMaker, Claude and Azure comparison, Kubeflow, model registry, and cost analysis.
