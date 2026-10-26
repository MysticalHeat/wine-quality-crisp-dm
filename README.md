# Лабораторная работа №3 — Wine Quality / CRISP-DM

**Елманов И. В., МИК21.** Преподаватель: Трубчик И. С.

[Открыть ноутбук на GitHub](https://github.com/MysticalHeat/wine-quality-crisp-dm/blob/main/Lab3_Wine_Quality_CRISP_DM.ipynb)
· [Открыть в Google Colab](https://colab.research.google.com/github/MysticalHeat/wine-quality-crisp-dm/blob/main/Lab3_Wine_Quality_CRISP_DM.ipynb)

Основной файл для сдачи: **`Lab3_Wine_Quality_CRISP_DM.ipynb`**.
Он содержит пояснения на русском языке, исполненный код, таблицы и графики.
`Lab3_Wine_Quality_CRISP_DM.html` — автономная версия для просмотра в браузере.

## Результаты

Источник — [Wine Quality, rajyellow46](https://www.kaggle.com/datasets/rajyellow46/wine-quality),
версия 1, именно объединённый `winequalityN.csv` из задания.
Задача — регрессия экспертной оценки `quality` по физико-химическим признакам и типу вина.

- Исходно 6 497 строк; удалено 1 168 полных дубликатов.
- Train: 4 263 строки; test: 1 066 строк. Одинаковые исходные признаки не пересекаются.
- Подбор на train: 5-fold GroupKFold; медианы, кодирование и масштабирование внутри Pipeline.
- Сравнение: Dummy, Ridge, Random Forest, HistGradientBoosting.
- По CV выбрана Random Forest, `min_samples_leaf=1`, 180 деревьев.
- Test MAE: **0.5284** против **0.6576** у Dummy; снижение на **19.64%**.
- Test RMSE: **0.6852**; R²: **0.3929**.
- Доля ошибок ≤1 балла: 86.49% у модели и 92.40% у Dummy. Превосходства по этой
  дополнительной метрике нет; это явно разобрано в ноутбуке.

## Запуск

В Google Colab: **Файл → Загрузить блокнот** → выбрать `.ipynb` → **Выполнить всё**.
При отсутствии CSV данные скачиваются автоматически, без ключа Kaggle.
Нужен доступ к интернету; сверяется SHA-256 исходного CSV.

Локально (рекомендуется Python 3.13):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python execute_notebook.py
python -m nbconvert --to html --embed-images Lab3_Wine_Quality_CRISP_DM.ipynb
```

`requirements.txt` фиксирует версии проверенного окружения. Для Colab с уже
установленными совместимыми библиотеками установка этих точных версий обычно не нужна.

## Состав

- `Lab3_Wine_Quality_CRISP_DM.ipynb` — выполненный ноутбук.
- `Lab3_Wine_Quality_CRISP_DM.html` — его автономное HTML-представление.
- `winequalityN.csv` — проверенный исходный CSV из Kaggle.
- `artifacts/results.json` — параметры, версии и итоговые метрики.
- `artifacts/*.csv` — CV, разбиение, прогнозы, метрики и важности признаков.
- `artifacts/wine_quality_pipeline.joblib` — pipeline, обученный на train;
  создаётся при выполнении ноутбука, в репозиторий не включён.
- `execute_notebook.py` — выполнение всех ячеек и сохранение результатов.
- `verify_results.py` — проверка структуры ноутбука, разбиения и пересчёт метрик.

Загрузка joblib требует совместимых версий библиотек. Загружать следует только
доверенные файлы. Для переноса на другую версию Python удобнее переисполнить ноутбук.

## Сдача

[Страница задания](https://do.skif.donstu.ru/mod/assign/view.php?id=107173).
Срок, показанный на ДО.СКИФ: **27.10.2026 00:00**.
В ответ требуется ссылка на GitHub или Colab с доступом всем, у кого она есть.
Сам локальный файл без опубликованной ссылки этому формату сдачи не соответствует.
