from src.visualizer import Visualizer
from pathlib import Path

def test_get_analytics():
    # Готовая дата
    classified_data = {
        Path(".\\test\\test_data\\test_emails_for_reader\\another_name.txt"): 'support requests',
        Path(".\\test\\test_data\\test_emails_for_reader\\mail_0001.txt"): 'support requests',
        Path(".\\test\\test_data\\test_emails_for_reader\\mail_0004.txt"): 'support requests',
        Path(".\\test\\test_data\\test_emails_for_reader\\mail_0037.txt"): 'work requests',
        Path(".\\test\\test_data\\test_emails_for_reader\\mail_0041.txt"): 'other',
        Path(".\\test\\test_data\\test_emails_for_reader\\mail_0045.txt"): 'other',
        Path(".\\test\\test_data\\test_emails_for_reader\\mail_0093.txt"): 'spam',
        Path(".\\test\\test_data\\test_emails_for_reader\\mail_0094.txt"): 'support requests',
        Path(".\\test\\test_data\\test_emails_for_reader\\mail_0095.txt"): 'work requests',
        Path(".\\test\\test_data\\test_emails_for_reader\\mail_0096.txt"): 'work requests',
        Path(".\\test\\test_data\\test_emails_for_reader\\mail_0097.txt"): 'support requests',
        Path(".\\test\\test_data\\test_emails_for_reader\\mail_0098.txt"): 'support requests',
        Path(".\\test\\test_data\\test_emails_for_reader\\mail_0099.txt"): 'work requests',
        Path(".\\test\\test_data\\test_emails_for_reader\\exe_expansion.exe"): 'broken',
        Path(".\\test\\test_data\\test_emails_for_reader\\json_expansion.json"): 'broken',
        Path(".\\test\\test_data\\test_emails_for_reader\\without_expansion"): 'broken',
    }

    visualizer = Visualizer(classified_data)

    right_data = {
        'support requests': 6,
        'work requests': 4,
        'other': 2,
        'spam': 1,
        'broken': 3
    }
    # Проверяем, правильно ли делает аналитику
    assert visualizer.get_analytics(classified_data) == right_data
