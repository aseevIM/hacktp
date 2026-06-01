import argparse
import sys
import json
from pathlib import Path
from email_class import Email
from email_Importer import EmailImporter
from classifier import Classifier
from main import Distributor
from visualizer import Visualizer
from logger import make_logger


def parse_arguments():
    """Парсит аргументы командной строки"""
    parser = argparse.ArgumentParser(
        description="Автоматизированная система обработки корпоративной почты"
    )
    parser.add_argument(
        "--inbox",
        type=str,
        required=True,
        help="Путь к папке с входящими письмами"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Путь к папке для результатов (sorted, logs, reports)"
    )
    parser.add_argument(
        "--rules",
        type=str,
        default="rules.json",
        help="Путь к JSON-файлу с правилами классификации"
    )
    parser.add_argument(
        "--sub-points",
        type=int,
        default=3,
        help="Вес ключевого слова в теме письма (по умолчанию 3)"
    )
    parser.add_argument(
        "--text-points",
        type=int,
        default=1,
        help="Вес ключевого слова в теле письма (по умолчанию 1)"
    )
    parser.add_argument(
        "--chart",
        type=str,
        choices=["bar", "pie"],
        default="bar",
        help="Тип диаграммы: bar (столбчатая) или pie (круговая)"
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    # начинаем! тут мы настраиваем логгер
    logger = make_logger(args.output)
    logger.info("=" * 50)
    logger.info("Запуск системы обработки корпоративной почты")
    logger.info(f"Входная папка: {args.inbox}")
    logger.info(f"Выходная папка: {args.output}")
    logger.info("=" * 50)

    # тут проверяем существование папки
    inbox_path = Path(args.inbox)
    if not inbox_path.exists():
        logger.error(f"Папка {args.inbox} не существует")
        sys.exit(1)

    # тут запускаем наш считыватель и читаем письма
    logger.info("Чтение писем...")
    importer = EmailImporter(input_dir=args.inbox)
    try:
        emails = importer.read_all_emails()
        logger.info(f"Прочитано писем: {len(emails)}")
    except Exception as e:
        logger.error(f"Ошибка при чтении писем: {e}")
        sys.exit(1)

    if len(emails) == 0:
        logger.warning("Не найдено писем для обработки")
        sys.exit(0)

    # классифицируем...
    logger.info("Классификация писем...")
    try:
        classifier = Classifier(
            emails=emails,
            rules_path=args.rules,
            sub_points=args.sub_points,
            text_points=args.text_points
        )
        classifier.classify_all()
        classified_data = classifier.get_email_to_category()
        logger.info(f"Классифицировано писем: {len(classified_data)}")

        # выводим статистику, благо логгер есть, почему бы и не вывести)
        stats_temp = {}
        for category in classified_data.values():
            stats_temp[category] = stats_temp.get(category, 0) + 1
        logger.info("Результаты классификации:")
        for category, count in sorted(stats_temp.items(), key=lambda x: -x[1]):
            logger.info(f"  {category}: {count}")

    except FileNotFoundError as e:
        logger.error(f"Файл правил не найден: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка в JSON файле правил: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Ошибка при классификации: {e}")
        sys.exit(1)

    # распределяем по папку с помощью distributor-a
    logger.info("Распределение файлов...")
    output_path = Path(args.output)
    distributor = Distributor(output_dir=output_path)

    try:
        distributor.distribute_all(classified_data)
        # используем логгер для ошибок
    except TypeError as e:
        logger.error(f"Ошибка в данных для распределения: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Неожиданная ошибка при распределении: {e}")
        sys.exit(1)

    # наше расширение!
    logger.info("Генерация отчёта...")
    try:
        visualizer = Visualizer(classified_data)
        report_dir = output_path / "reports"
        report_path = visualizer.save_to_html(report_dir, args.chart)
        logger.info(f"Отчёт сохранён: {report_path}")
    except Exception as e:
        logger.warning(f"Не удалось сгенерировать отчёт: {e}")
        logger.info("Программа продолжает работу без отчёта")

    # обработка завершена блаблабла
    logger.info("=" * 50)
    logger.info("ОБРАБОТКА ЗАВЕРШЕНА")

    # ФИНАЛ! Считаем статы
    stats = {}
    for category in classified_data.values():
        stats[category] = stats.get(category, 0) + 1

    logger.info("Итоговая статистика по категориям:")
    for category, count in sorted(stats.items(), key=lambda x: -x[1]):
        logger.info(f"  {category}: {count}")
    logger.info(f"Всего обработано: {len(classified_data)}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()