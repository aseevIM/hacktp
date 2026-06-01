from email_class import Email
from pathlib import Path

STANDART_PATH = "......."

class EmailImporter:
    def __init__(self, input_dir = STANDART_PATH):
        # возможные варианты записи конкретных полей, беру только поле subject, остальные не несут никакой
        # важной для классификации информации
        # !!!! Обсудить
        self.subject_v = {"тема", "subject", "tema"}
        self.input_dir = input_dir

    # Читает все письма, возвращает список экземпляров Email
    def read_all_emails(self):
        emails = []

        for file_path in Path(self.input_dir).iterdir():
            email = self.read_email(file_path)
            emails.append(email)

        return emails
        # !!! Добавить обработку ошибок, битых файлов и тд

    #Прочитать одно письмо, вернуть в виде экземпляра класса Email, вспомогательный
    def read_email(self, file_path):
        subject = ""
        text = []
        is_main_text = False

        with open(file_path, encoding="utf-8") as file:
            lines = file.read().splitlines()

        for line in lines:
            line = line.lower()

            # Добавляем строку в текст, если она не пустая
            if is_main_text and line.strip()!= "":
                text.append(line)
                continue

            # Если есть индикатор темы, считываем eё
            if any(x for x in self.subject_v if x in line):
                subject = line.split(":", 1)[1]
                is_main_text = True

        # переводим полученый текст в строку
        text = "\n".join(text)
        # Возвращаем
        email = Email(file_path.name, file_path, subject, text)
        return email



# ТЕСТ
if __name__ == "__main__":
    reader = EmailImporter()
    emails = reader.read_all_emails()

    print(f"Всего прочитано писем: {len(emails)}")
    print("-" * 40)

    for email in emails:
        print(f"Файл   : {email.file_name}")
        print(f"Тема   : {email.subject}")
        print(f"Текст  : {email.text}...")
        print("")