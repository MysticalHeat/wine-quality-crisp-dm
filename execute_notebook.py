"""Выполнить все ячейки и сохранить результаты для просмотра без ядра."""

import os
from pathlib import Path

# Ограничиваем внутренний параллелизм численных библиотек, чтобы CV не
# создавал вложенные пулы на всех ядрах машины.
for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[variable] = '1'

import nbformat
from nbclient import NotebookClient

root = Path(__file__).parent.resolve()
path = root / 'Lab3_Wine_Quality_CRISP_DM.ipynb'
notebook = nbformat.read(path, as_version=4)
client = NotebookClient(
    notebook,
    timeout=600,
    kernel_name='python3',
    resources={'metadata': {'path': str(root)}},
)
client.execute()
nbformat.validate(notebook)
nbformat.write(notebook, path)
print('Все ячейки выполнены:', path)
