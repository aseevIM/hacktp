class Classifier:
    # Принимаю в качестве аргумента все письма(нужно создать под них класс) и файл правил
    def __init__(self, emails, rules_path):
        self.emails = emails
        self.rules_to_categorize = self.get_rules_to_categorize(rules_path)

    # Классифицирует все предоставленные письма, сохраняет в поле класса
    def classify_all(self):
        pass

    # Классифицирует конкретное письмо, вспомогательный
    def classify(self, email):
        pass

    # Возвращает результат в формате: Путь -> Категория
    def get_email_to_category(self):
        pass

    # Возвращает результат в формате: Категория -> Количество писем, также общее количество писем
    def get_analytics(self):
        pass

    # Получает правила для распределения писем на категории (думаю сделать через json файл)
    def get_rules_to_categorize(self, path):
        pass