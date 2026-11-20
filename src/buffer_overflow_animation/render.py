import argparse
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Универсальный скрипт для рендера анимаций Manim"
    )
    parser.add_argument(
        "file",
        nargs="?",
        default="animation.py",
        help="Путь к файлу сценария (по умолчанию: animation.py)",
    )
    parser.add_argument(
        "scene",
        nargs="?",
        default="BufferOverflowScene",
        help="Имя класса сцены (по умолчанию: BufferOverflowScene)",
    )

    # Качество рендеринга
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-l",
        "--low",
        action="store_true",
        help="Низкое качество (480p15) — быстро для тестов",
    )
    group.add_argument(
        "-m",
        "--medium",
        action="store_true",
        help="Среднее качество (720p30)",
    )
    group.add_argument(
        "-h_q",
        "--high",
        action="store_true",
        help="Высокое качество (1080p60) — для сдачи (по умолчанию)",
    )
    group.add_argument(
        "-4k", "--fourk", action="store_true", help="Ультра качество (2160p60 4K)"
    )

    # Дополнительные флаги
    parser.add_argument(
        "-p",
        "--preview",
        action="store_true",
        default=True,
        help="Автоматически запустить видео после рендера (по умолчанию: вкл)",
    )
    parser.add_argument(
        "--no-preview",
        dest="preview",
        action="store_false",
        help="Не запускать плеер после рендера",
    )
    parser.add_argument(
        "-k",
        "--keep",
        action="store_true",
        help="Сохранять промежуточные кадры/файлы",
    )

    args = parser.parse_args()

    # Формируем флаги качества для Manim
    quality_flag = "-qh"  # По умолчанию Full HD
    if args.low:
        quality_flag = "-ql"
    elif args.medium:
        quality_flag = "-qm"
    elif args.high:
        quality_flag = "-qh"
    elif args.fourk:
        quality_flag = "-qk"

    # Собираем команду manim
    cmd = ["manim"]
    if args.preview:
        cmd.append("-p")
    cmd.append(quality_flag)

    if args.keep:
        cmd.append("--save_pngs")

    cmd.extend([args.file, args.scene])

    print(f"▶ Запуск рендеринга: {' '.join(cmd)}")
    print("-" * 50)

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[Ошибка] Рендеринг завершился с кодом {e.returncode}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(
            "\n[Ошибка] Команда 'manim' не найдена. Убедись, что активировано виртуальное окружение и установлен manim."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
    