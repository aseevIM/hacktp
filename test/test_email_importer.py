from src.email_Importer import EmailImporter
from src.email_class import Email
import pytest
from pathlib import Path


def test_read_all_emails():
    # Правильные экземпляры писем
    emails = [
        Email("another_name.txt", Path(".\\test\\test_data\\test_emails_for_reader\\another_name.txt"), "", "from: o.belova@client.biz\nдобрый день.\nу нас критичный инцидент: корпоративный портал возвращает ошибку 500 уже 40 минут. затронуты примерно 15 сотрудников. просим срочно проверить.\notpravleno s iphone"),
        Email("mail_0001.txt", Path(".\\test\\test_data\\test_emails_for_reader\\mail_0001.txt"), "браузер chrome зависает при открытии", "from: s.volkov@partner.ru\nздравствуйте!\nпосле обновления системы браузер chrome не открывает файлы нужного формата. раньше всё работало.\nспасибо."),
        Email("mail_0004.txt", Path(".\\test\\test_data\\test_emails_for_reader\\mail_0004.txt"), "падает система согласования, работа остановлена", "от кого: виктор громов <v.gromov@partner.ru>\nкому: it-support@company.ru\nдата: 28.01.2025 18:19\nдобрый день.\nу нас критичный инцидент: система согласования возвращает ошибку 500 уже 40 минут. затронуты примерно 15 сотрудников. просим срочно проверить.\nесли вопрос не к вам — перенаправьте, пожалуйста.\nприкрепил: contract_v2.docx"),
        Email("mail_0037.txt", Path(".\\test\\test_data\\test_emails_for_reader\\mail_0037.txt"), "счёт на оплату №8141", "from: noreply@jira.internal\nhi,\nпросим подтвердить получение счёта №8141. оплата по договору должна пройти до 26.1.2025.\nспасибо.\nвложение: invoice.pdf"),
        Email("mail_0041.txt", Path(".\\test\\test_data\\test_emails_for_reader\\mail_0041.txt"), "вы выиграли iphone 15!", "from: a.kozlov@company.ru\nздравствуйте!\nдорогой пользователь! ваш аккаунт будет заблокирован через 24 часа. для подтверждения личности немедленно введите логин и пароль: http://secure-login-verify.net\nid заявки: #64548"),
        Email("mail_0045.txt", Path(".\\test\\test_data\\test_emails_for_reader\\mail_0045.txt"), "", "from: елена новикова <e.novikova@corp.local>\nto: it-support@company.ru\ndate: 2025-04-30 12:44\nпустышка ааааааааа\nдаывлпавщыапрвпщзлфвзапоыврж\nыврофплрапз ыншг анкшцгу гцгн уцк нцгушнпашгц айцу шщ"),
        Email("mail_0093.txt", Path(".\\test\\test_data\\test_emails_for_reader\\mail_0093.txt"), "re: exclusive offer — limited time", "from: a.kozlov@company.ru\nпоздравляем! вы стали победителем розыгрыша. для получения приза перейдите по ссылке: http://totally-not-spam.ru/prize и введите данные банковской карты.\np.s. это уже второй запрос по данной теме.\nво вложении: screenshot.png"),
        Email("mail_0094.txt", Path(".\\test\\test_data\\test_emails_for_reader\\mail_0094.txt"), "критический инцидент — bi-система недоступен", "from: alerts <alerts@grafana.internal>\nto: it-support@company.ru\ndate: 2025-06-10 09:49\nздравствуйте!\nпосле утреннего обновления bi-система перестал открываться у всего отдела юристы. ошибка появляется сразу при входе. работа полностью остановлена, нужна срочная помощь.\notpravleno s iphone\nфайл: error_log.txt\nid заявки: #99742"),
        Email("mail_0095.txt", Path(".\\test\\test_data\\test_emails_for_reader\\mail_0095.txt"), "запрос доступа к 1c", "from: алексей козлов <a.kozlov@company.ru>\nto: it-support@company.ru\ndate: 2025-04-28 08:18\nколлеги, привет!\nпосле перевода в отдел продажи у мария смирнова пропал доступ к 1c. раньше всё работало. прошу восстановить.\notpravleno s iphone\nприкрепил: contract_v2.docx\nкод ошибки: err_762"),
        Email("mail_0096.txt", Path(".\\test\\test_data\\test_emails_for_reader\\mail_0096.txt"), "поиск работы", "from: emelya@slavyane.com\nдобрый день.\nэто отклик на должность сотрудника супер пупер дупер ультра мега дипер трипер важный холст бумажный pip специалиста"),
        Email("mail_0097.txt", Path(".\\test\\test_data\\test_emails_for_reader\\mail_0097.txt"), "проблема с мышь", "from: kate brown <k.brown@extern.org>\nto: it-support@company.ru\ndate: 2025-01-21 14:38\nздравствуйте!\nу сотрудника наталья лебедева мышь издаёт посторонние звуки. просим организовать диагностику или замену.\nс уважением,\nнаталья лебедева\nво вложении: screenshot.png"),
        Email("mail_0098.txt", Path(".\\test\\test_data\\test_emails_for_reader\\mail_0098.txt"), "неисправность оборудования: ноутбук", "from: тимур андреев <t.andreev@company.ru>\nto: it-support@company.ru\ndate: 2025-06-07 14:17\nhi,\nноутбук сломался экран с вчерашнего дня. пробовал перезагрузить — не помогло. нужна помощь.\np.s. это уже второй запрос по данной теме."),
        Email("mail_0099.txt", Path(".\\test\\test_data\\test_emails_for_reader\\mail_0099.txt"), "fwd: запрос доступа к vpn", "from: дмитрий орлов <d.orlov@corp.local>\nto: it-support@company.ru\ndate: 2025-01-18 11:49\nздравствуйте!\n---------- forwarded message ---------\nfrom: alerts\nsubject: запрос доступа к vpn\nновый сотрудник тимур андреев приступает к работе с понедельника. нужно подготовить доступ к vpn и корпоративной почте.\n---\nперенаправляю вам, так как не знаю, к кому именно обращаться.\nbest regards,\nтимур андреев"),
    ]

    # Создаём класс и проверяем правильно ли считывает
    reader = EmailImporter(".\\test\\test_data\\test_emails_for_reader")
    assert reader.read_all_emails() == emails

