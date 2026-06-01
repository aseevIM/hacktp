import logging

# Создает и настраивает logger, (для main)

# !!!! разобраться со стандартной out директорией
def make_logger(output_dir="out"):
    logger = logging.getLogger("processor")

    # Доступны все уровни
    logger.setLevel(logging.DEBUG)

    # Формат выводимого текста
    formatt = logging.Formatter("%(asctime)s : %(levelname)s - %(filename)s - %(message)s")

    # файловый и консольный обработчик, чтобы выводить данные в консоль и файл
    f_handler = logging.FileHandler(f"{output_dir}/process.log", encoding="utf-8")
    c_handler = logging.StreamHandler()

    f_handler.setFormatter(formatt)
    c_handler.setFormatter(formatt)

    logger.addHandler(f_handler)
    logger.addHandler(c_handler)

    return logger
