"""Проверка целостности выполненного ноутбука и независимый пересчёт метрик."""

import json
from pathlib import Path

import nbformat
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


root = Path(__file__).parent
notebook_path = root / 'Lab3_Wine_Quality_CRISP_DM.ipynb'
notebook = nbformat.read(notebook_path, as_version=4)
nbformat.validate(notebook)
code_cells = [cell for cell in notebook.cells if cell.cell_type == 'code']
assert all(cell.execution_count is not None for cell in code_cells)
outputs = [output for cell in code_cells for output in cell.outputs]
assert not any(output.output_type == 'error' for output in outputs)
plots = sum('image/png' in output.get('data', {}) for output in outputs)
assert plots >= 5

artifacts = root / 'artifacts'
report = json.loads((artifacts / 'results.json').read_text(encoding='utf-8'))
split = pd.read_csv(artifacts / 'split.csv', dtype={'group': str})
train_groups = set(split.loc[split['split'] == 'train', 'group'])
test_groups = set(split.loc[split['split'] == 'test', 'group'])
assert train_groups.isdisjoint(test_groups)
predictions = pd.read_csv(artifacts / 'test_predictions.csv')
test_indices = set(split.loc[split['split'] == 'test', 'row_after_dedup'])
assert set(predictions['row_after_dedup']) == test_indices
assert len(predictions) == report['test_rows']
actual, predicted = predictions['actual'], predictions['predicted']
recalculated = {
    'MAE': mean_absolute_error(actual, predicted),
    'RMSE': np.sqrt(mean_squared_error(actual, predicted)),
    'R2': r2_score(actual, predicted),
    'within_1': np.mean(np.abs(actual - predicted) <= 1),
}
for metric, value in recalculated.items():
    assert np.isclose(value, report['test_metrics'][metric]), metric
cv = pd.read_csv(artifacts / 'cv_comparison.csv').sort_values('CV MAE')
assert cv.iloc[0]['model'] == report['selected_model']
assert np.isclose(cv.iloc[0]['CV MAE'], report['cv_mae'])
assert report['raw_rows'] - report['duplicates_removed'] == len(split)
assert (root / 'Lab3_Wine_Quality_CRISP_DM.html').is_file()
print(f'Проверки пройдены: {len(code_cells)} исполненных ячеек, {plots} графических выводов.')
print('Пересечение групп: 0. Метрики независимо пересчитаны по CSV прогнозов.')
for filename in ('Lab3_Wine_Quality_CRISP_DM.ipynb', 'Lab3_Wine_Quality_CRISP_DM.html'):
    path = root / filename
    print(f'{path.stat().st_size:,} bytes: {path.resolve().as_uri()}')
