## Запуск приложения

1. Создание виртуального окружения:
```
conda create -n py38_webapp_env python=3.8
conda activate py38_webapp_env
```

2. Установка нужных библиотек:
```
pip install -r requirements.txt
```

3. Настройка датабазы:
```
export FLASK_APP=main.py
flask db init
flask db migrate
flask db upgrade
```

4. Запуск приложения:

```
python main.py
```
Итого, приложение было запущено на http://localhost:5000/