# Operation, temperature and duration extraction from catalyst synthesis paragraphs

Code for a paper currently under submission. The reference will be added on publication.

The framework reads the preparation paragraph of a catalysis paper and reports each synthesis
event as a record of **operation, temperature and duration**, with the heating rate and the
vessel when the text states them. It is built on ChemDataExtractor 2 and two Snowball relation
models (`OperationTemperature`, `OperationTime`) trained on annotated events. This repository
covers training and evaluation on the validation set.

## Files

| File | Description |
|---|---|
| `000_Visualization_preparation.ipynb` | Training-set composition (operation frequencies, per-year counts), reporting-practice analysis for calcination, and the training event sheet used by 001 |
| `001_Snowball_Training.ipynb` | Builds seed records from the annotated temperature and time spans and the operation vocabulary from the training triggers, then trains the two Snowball models |
| `002_Extraction_Validation.ipynb` | Extracts operation / temperature / duration records from the validation paragraphs |
| `003_Performance_Validation.ipynb` | Scores the extracted records against the validation annotations |
| `operation_model.py` | ChemDataExtractor model definitions imported by 001 and 002 |

## Installation

Tested on Windows 10, Python 3.9.

```bash
conda create -n synth_extract python=3.9
conda activate synth_extract
pip install chemdataextractor2==2.4.0 pandas==2.3.2 numpy==1.26.4 matplotlib==3.9.4 openpyxl==3.1.5 jupyterlab==4.5.3
```

## Input data

The code runs on the synthesis paragraphs of published articles. The paragraphs are extracted
automatically through the publishers' APIs with
[Structured_Data_Extraction](https://github.com/Ismail-Salim/Structured_Data_Extraction).
The annotation files are provided with the paper; the paragraph text is not redistributed and
must be re-extracted by the user.

## Running

Run the notebooks in order from this folder. Each notebook reads the files written by the
previous one.

| Step | Notebook | Main outputs |
|---|---|---|
| 0 | `000_Visualization_preparation.ipynb` | `training_events_all_operations.xlsx`, figures in `full_table_visualizations/` |
| 1 | `001_Snowball_Training.ipynb` | `OperationTemperature_list.pkl`, `OperationTime_list.pkl`, `positive_operation_events.csv`, `Snowball_model/` |
| 2 | `002_Extraction_Validation.ipynb` | `operation_results_ALL/operation_temperature_time_final_compact.xlsx` |
| 3 | `003_Performance_Validation.ipynb` | `performance_evaluation_tables.xlsx` |

Seed records are shuffled with a fixed seed (`SEED_RECORDS_RANDOM_SEED = 42`), so repeated runs
train the same models.

### Extraction (002)

1. The preparation paragraph is Unicode-normalised (degree signs, dashes, zero-width
   characters) and cut at the first characterization or testing heading.
2. ChemDataExtractor splits it into sentences. A sentence is parsed when it contains an
   operation term from the training vocabulary and a temperature or duration value.
3. `OperationTemperature` returns (operation, temperature) records and `OperationTime`
   returns (operation, duration) records.
4. A value followed by a time unit (`5 °C/min`) is a heating rate, never a temperature.
5. Within a sentence, each duration is paired with at most one temperature record, best pair
   first. A duration that no temperature claims is reported on its own.
6. Each heating rate is bound to the event whose set point is nearest to it.
7. A heating, thermal hold or thermal treatment step in a sealed vessel is reported as
   hydrothermal treatment.

The method switches are in the first cell of 002 and are all on for the reported results.

### Scoring (003)

- Predicted and annotated records are compared per paper, as multisets of keys.
- Criteria: temperature, duration, temperature–duration pairing, operation–temperature
  pairing, operation–duration pairing, the full (operation, temperature, duration) triple,
  and four heating-rate criteria. Precision, recall and F1 are reported for each.
- Only numeric values are scored. Temperatures are compared in their written unit (°C or K);
  a range keys on its lower bound.
- Events with no operation trigger of their own are excluded.

## Citation

The paper is under submission; citation details will be added on publication.

## License

MIT
