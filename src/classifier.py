from pathlib import Path
import json
from pathlib import Path

# подгружаем логгер
import logging
logger = logging.getLogger("processor")

class Classifier:
    # Принимаю в качестве аргумента все письма, файл правил, вес темы и текста письма
    def __init__(self, emails, rules_path,  sub_points, text_points):
        # Дополнительная проверка списка
        if type(emails) != list:
            logger.error(f"emails должен быть списком, получен {type(emails)}")
            raise TypeError(f"emails должен быть списком, получен {type(emails)}")
        if len(emails) == 0:
            logger.warning("Получен пустой список писем")
        self.emails = emails

        self.rules_to_categorize = self.get_rules_to_categorize(rules_path)

        self.sub_points = sub_points
        self.text_points = text_points

        self.result = {}

    # Классифицирует все предоставленные письма, сохраняет в поле result класса
    def classify_all(self):
        print(self.rules_to_categorize)
        logger.info("Начата классификация писем")
        for email in self.emails:
            category = self.classify(email)
            self.result[email.path] = category
        logger.info("Классификация писем завершена")


    # Классифицирует конкретное письмо, вспомогательный
    def classify(self, email):
        text = email.text.lower()
        subject = email.subject.lower()
        points = {}

        for category, key_words in self.rules_to_categorize.items():
            score = 0

            # Выдаем письму очки при нахождении в тексте ключевых слов конкретной категории
            score += sum(self.sub_points for word in key_words if word in subject)
            score += sum(self.text_points for word in key_words if word in text)

            points[category] = score

        # Выбираем категорию с наивысшим баллом
        highest_score = max(points.values())
        # Если не попадает ни под одну кидаем в other
        if highest_score == 0:
            return "other"

        most_likely_category = [x for x, val in points.items() if val == highest_score]
        logger.info(f"Классификация письма {email.path} завершена, присвоена категория {most_likely_category[0]}")
        return most_likely_category[0]

    # Возвращает результат в формате: Путь -> Категори
    def get_email_to_category(self):
        return self.result

    # Получает правила для распределения писем на категории
    def get_rules_to_categorize(self, path):

        # Доп проверка на наличие файла
        if not Path(path).exists():
            logger.error(f"Файл Правил не существует по указанному пути: '{path}'")
            raise FileNotFoundError(f"Файл правил не найден: '{path}'")

        # Проверка расширения файла
        if Path(path).suffix != ".json":
            logger.error(f"Файл по пути: '{path}' не является json файлом")
            raise ValueError(f"Файл по пути: '{path}' не является json файлом")

        with open(path, encoding='utf-8') as file:
            logger.info(f"Загрузка правил из файла: '{path}'")
            try:
                rules = json.load(file)
                logger.info(f"Правила загружены")
                return rules
            # файл не работает
            except json.JSONDecodeError as e:
                logger.info(f"Ошибка при чтении файла {e}")
                raise ValueError(f"Ошибка при чтении файла")



