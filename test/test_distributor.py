from src.distributor import Distributor
from pathlib import Path
import shutil
import os
import filecmp


# Копируем письма в отдельную папку, чтобы не поломать тесты email_importer
def copy_emails():
    folder_from = Path(".\\test\\test_data\\test_emails_for_reader")
    folder_to = Path(".\\test\\test_data\\test_emails_for_distributor")

    for file in os.listdir(folder_from):
        shutil.copy(os.path.join(folder_from, file), os.path.join(folder_to, file))


# Функция отчищает папку с заданным путём
def clean_folder(path):
    for i in os.listdir(path):
        item_path = os.path.join(path, i)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)


def test_classify_all():
    # Создаём экземпляр класса
    distributor = Distributor(Path(".\\test\\test_data\\test_output"))

    # Готовая дата
    classified_data = {
        Path(".\\test\\test_data\\test_emails_for_distributor\\another_name.txt"): 'support requests',
        Path(".\\test\\test_data\\test_emails_for_distributor\\mail_0001.txt"): 'support requests',
        Path(".\\test\\test_data\\test_emails_for_distributor\\mail_0004.txt"): 'support requests',
        Path(".\\test\\test_data\\test_emails_for_distributor\\mail_0037.txt"): 'work requests',
        Path(".\\test\\test_data\\test_emails_for_distributor\\mail_0041.txt"): 'other',
        Path(".\\test\\test_data\\test_emails_for_distributor\\mail_0045.txt"): 'other',
        Path(".\\test\\test_data\\test_emails_for_distributor\\mail_0093.txt"): 'spam',
        Path(".\\test\\test_data\\test_emails_for_distributor\\mail_0094.txt"): 'support requests',
        Path(".\\test\\test_data\\test_emails_for_distributor\\mail_0095.txt"): 'work requests',
        Path(".\\test\\test_data\\test_emails_for_distributor\\mail_0096.txt"): 'work requests',
        Path(".\\test\\test_data\\test_emails_for_distributor\\mail_0097.txt"): 'support requests',
        Path(".\\test\\test_data\\test_emails_for_distributor\\mail_0098.txt"): 'support requests',
        Path(".\\test\\test_data\\test_emails_for_distributor\\mail_0099.txt"): 'work requests'
    }

    # Очищаем папки
    clean_folder(Path(".\\test\\test_data\\test_output"))
    clean_folder(Path(".\\test\\test_data\\test_emails_for_distributor"))

    # Копируем письма, которые будут распределяться и распределяем
    copy_emails()
    distributor.distribute_all(classified_data)
    distributor.distribute_remaining_files(".\\test\\test_data\\test_emails_for_distributor", "broken")


    # Сверяем правильное распределение с получившимся
    output_data = ".\\test\\test_data\\test_output"
    right_data = ".\\test\\test_data\\rigth_distributed_emails"
    difference = filecmp.dircmp(output_data, right_data)
    assert len(difference.left_only) + len(difference.right_only) + len(difference.diff_files) == 0
