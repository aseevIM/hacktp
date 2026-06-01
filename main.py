from pathlib import Path

from src.classifier import Classifier
from src.distributor import Distributor
from src.email_Importer import EmailImporter
from src.logger import make_logger
from src.visualizer import Visualizer


# аргументы
class Config:
    def __init__(self):
        self.rules_path = None
        self.inbox_path = None

        self.logs_output_path = None
        self.report_path = None
        self.classified_emails_path = None

        self.subject_points = None
        self.text_points = None
        self.chart_type = None

    # значения по умолчанию
    def set_by_default(self):
        #корень проекта
        root = Path(__file__).resolve().parent

        self.rules_path = root / "data" / "rules" / "rules.json"
        self.inbox_path = root / "data" / "inbox"

        self.logs_output_path = root / "output" / "logs"
        self.report_path = root / "output" / "table"
        self.classified_emails_path = root / "output" / "classified"

        self.subject_points = 2
        self.text_points = 1
        self.chart_type = "bar"

    # кастомные значения
    def set_by_user(self, rules_path, inbox_path, logs_output_path,
                    report_path, classified_emails_path, subject_points, text_points, chart_type):
        self.rules_path = rules_path
        self.inbox_path = inbox_path

        self.logs_output_path = logs_output_path
        self.report_path = report_path
        self.classified_emails_path = classified_emails_path

        self.subject_points = subject_points
        self.text_points = text_points
        self.chart_type = chart_type

def change_arguments(arguments:Config):
    arguments.set_by_default()

    print("Выберите тип взаимодействия с системой изменения аргументов:")
    print("1 - Оставить значения по умолчанию")
    print("2 - Изменить параметры через консоль")
    print("3 - Изменить параметры через графический интерфейс")
    print("Остальное - Выход из программы")

    prefer = input().strip()
    if prefer == "1":
        return
    elif prefer == "2":
        term_change(arguments)
    elif prefer == "3":
        gui_change(arguments)
    else:
        exit()

def term_change(arguments:Config):
    try:
        path = input("json файл правил категоризации: ").strip()
        if path:
            path = Path(path)
            if path.suffix == ".json":
                arguments.rules_path = path
            else:
                print("Неверное расширение файла, оставлено значение по умолчанию")
    except Exception as e:
        print(f"Ошибка: {e}, установлено значение по умолчанию")

    try:
        path = input("Папка с письмами: ").strip()
        if path:
            arguments.inbox_path = Path(path)
    except Exception as e:
        print(f"Ошибка: {e}, установлено значение по умолчанию")

    try:
        path = input("Папка для логов: ").strip()
        if path:
            arguments.logs_output_path = Path(path)
    except Exception as e:
        print(f"Ошибка: {e}, установлено значение по умолчанию")

    try:
        path = input("Папка для отчётов: ").strip()
        if path:
            arguments.report_path = Path(path)
    except Exception as e:
        print(f"Ошибка: {e}, установлено значение по умолчанию")

    try:
        path = input("Папка для распределённых писем: ").strip()
        if path:
            arguments.classified_emails_path = Path(path)
    except Exception as e:
        print(f"Ошибка: {e}, установлено значение по умолчанию")

    try:
        val = int(input("Баллы за совпадение с темой: ").strip())
        if val>=0:
            arguments.subject_points = val
    except Exception as e:
        print(f"Ошибка: {e}, установлено значение по умолчанию")

    try:
        val = int(input("Баллы за совпадение с основным текстом: ").strip())
        if val>=0:
            arguments.text_points = val
    except Exception as e:
        print(f"Ошибка: {e}, установлено значение по умолчанию")

    try:
        table = input("Тип диаграммы (bar или pie): ").strip().lower()
        if table in ("bar", "pie"):
            arguments.chart_type = table
        else:
            print("Неизвестный тип диаграммы, установлено значение по умолчанию")
    except Exception as e:
        print(f"Ошибка: {e}, установлено значение по умолчанию")

def gui_change(arguments: Config):
    pass

def main():
    arguments = Config()
    change_arguments(arguments)

    logger = make_logger(arguments.logs_output_path)

    logger.info("logger создан")
    logger.info("Программа начала свою работу")

    reader = EmailImporter(arguments.inbox_path)
    emails = reader.read_all_emails()

    classifier = Classifier(emails, arguments.rules_path, arguments.subject_points, arguments.text_points)
    classifier.classify_all()
    email_to_category = classifier.get_email_to_category()

    visualizer = Visualizer(email_to_category)
    visualizer.save_to_html(arguments.report_path, arguments.chart_type)

    distributor = Distributor(arguments.classified_emails_path)
    distributor.distribute_all(email_to_category)



    logger.info("программа успешно завершила свою работу")

if __name__ == "__main__":
    main()



