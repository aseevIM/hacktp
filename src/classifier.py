class Classifier:
    # Принимаю в качестве аргумента все письма(нужно создать под них класс), файл правил, вес темы и текста письма
    def __init__(self, emails, rules_path,  sub_points = 3, text_points = 1):
        self.emails = emails
        self.rules_to_categorize = self.get_rules_to_categorize(rules_path)

        self.sub_points = sub_points
        self.text_points = text_points

        self.result = {}

    # Классифицирует все предоставленные письма, сохраняет в поле result класса
    def classify_all(self):
        for email in self.emails:
            category = self.classify(email)
            self.result[email.path] = category


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
        return most_likely_category[0]

    # Возвращает результат в формате: Путь -> Категори
    def get_email_to_category(self):
        return self.result

    # Получает правила для распределения писем на категории (думаю сделать через json файл)
    def get_rules_to_categorize(self, path):
        pass