from email_class import Email
from pathlib import Path

import logging
logger = logging.getLogger("processor")

class EmailImporter:
    def __init__(self, input_dir = "inbox\\inbox"):
        # возможные варианты записи конкретных полей, беру только поле subject, остальные не несут никакой
        # важной для классификации информации

        self.subject_v = {"тема", "subject", "tema"}
        self.input_dir = input_dir

    # Читает все письма, возвращает список экземпляров Email
    def read_all_emails(self):
        logger.info("Начата обработка писем")
        emails = []

        for file_path in Path(self.input_dir).iterdir():
            # для пропуска директорий
            if not file_path.is_file():
                logger.warning(f"Пропущена директория: '{file_path}'")
                continue
            try:
                email = self.read_email(file_path)
                emails.append(email)
            except Exception as e:
                logger.exception(f"не удалось прочесть файл: '{file_path}', был пропущен")

        logger.info("Письма обработаны")
        return emails


    #Прочитать одно письмо, вернуть в виде экземпляра класса Email, вспомогательный
    def read_email(self, file_path):
        subject = ""
        text = []
        is_main_text = False

        if file_path.suffix != '.txt':
            raise ValueError("файл должен быть '.txt'")

        with open(file_path, encoding="utf-8") as file:
            lines = file.read().splitlines()

        # все кроме темы закидываем в текст
        for line in lines:
            line = line.lower()

            if not is_main_text:
                # Если есть индикатор темы, считываем eё
                if any(x for x in self.subject_v if x in line):
                    subject = line.split(":", 1)[1]
                    is_main_text = True
                    continue

            # Добавляем строку в текст, если она не пустая
            if line.strip()!= "":
                text.append(line)


        # переводим полученый текст в строку
        text = "\n".join(text)
        # Возвращаем
        email = Email(file_path.name, file_path, subject, text)

        logger.info(f"Файл '{file_path}' успешно прочитан")
        return email



# ТЕСТ
if __name__ == "__main__":
    reader = EmailImporter()
    emails = reader.read_all_emails()

    print(f"Всего прочитано писем: {len(emails)}")
    print("-" * 40)

