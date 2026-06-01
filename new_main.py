from hmac import new
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


def main():
    arguments = Config()
    change_arguments(arguments)

    logger = make_logger(arguments.logs_output_path)

    reader = EmailImporter(arguments.inbox_path)
    emails = reader.read_all_emails()

    classifier = Classifier(emails, arguments.rules_path, arguments.subject_points, arguments.text_points)
    classifier.classify_all()
    email_to_category = classifier.get_email_to_category()

    visualizer = Visualizer(email_to_category)
    visualizer.save_to_html(arguments.report_path, arguments.chart_type)

    distributor = Distributor(arguments.classified_emails_path)
    distributor.distribute_all(email_to_category)


if __name__ == "__main__":
    main()


