# Buffer Overflow Animation

Образовательная анимация на Python (Manim), демонстрирующая **переполнение буфера в стеке** — классическую уязвимость безопасности ПО.

## Что показывает анимация

### Часть 1: Нормальная работа
- Функция `vulnerable()` с буфером `char buf[8]`
- Корректный ввод `"AAAA"` (4 байта) — помещается в буфер
- Адрес возврата (`Return Address`) остается нетронутым → возврат в `main()`

### Часть 2: Эксплойт (переполнение)
- Ввод 24 байта: `"AAAAAAAAAAAAAAAA"` + адрес `malware_shell` (`0x401196`)
- Перезапись `Saved RBP` и `Return Address` в стеке
- При `return` управление прыгает в `malware_shell()` вместо `main()`

## Установка

```bash
# Клонирование
git clone https://github.com/<your-username>/buffer-overflow-animation.git
cd buffer-overflow-animation

# Виртуальное окружение + зависимости
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## Запуск

### Быстрый старт (через скрипт)
```bash
# Низкое качество (480p) — для тестов
python -m buffer_overflow_animation.render -l

# Среднее качество (720p)
python -m buffer_overflow_animation.render -m

# Высокое качество (1080p) — по умолчанию
python -m buffer_overflow_animation.render

# 4K (2160p60)
python -m buffer_overflow_animation.render --fourk

# Без автозапуска плеера
python -m buffer_overflow_animation.render --no-preview

# Сохранить промежуточные кадры
python -m buffer_overflow_animation.render -k
```

### Прямой запуск через Manim
```bash
# Низкое качество
manim -ql animation.py BufferOverflowScene

# Высокое качество + предпросмотр
manim -pqh animation.py BufferOverflowScene
```

## Структура проекта

```
buffer_overflow_animation/
├── src/
│   └── buffer_overflow_animation/
│       ├── __init__.py
│       ├── animation.py    # Основная сцена Manim
│       └── render.py       # Скрипт запуска рендеринга
├── media/                  # Генерируется при рендеринге (в .gitignore)
├── tests/
├── pyproject.toml
├── poetry.lock
└── README.md
```

## Требования

- Python 3.12+ 
- [Manim](https://www.manim.community/) 0.22.x
- FFmpeg (для рендеринга видео)
- LaTeX (опционально, для формул)

## Настройка качества

| Флаг | Качество | Разрешение | FPS | Назначение |
|------|----------|------------|-----|------------|
| `-ql` | Low | 854×480 | 15 | Быстрые тесты |
| `-qm` | Medium | 1280×720 | 30 | Предпросмотр |
| `-qh` | High | 1920×1080 | 60 | Продакшн (по умолчанию) |
| `-qk` | 4K | 3840×2160 | 60 | Высокое качество |

## Лицензия

MIT License — свободное использование в образовательных целях.
