import logging
from pathlib import Path

logger = logging.getLogger("processor")

class Distributor:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)

    def distribute_all(self, classified_data):
        if  type(classified_data) != dict:
            logger.error(f"classified_data должен быть словарём, a не {type(classified_data)}")
            raise TypeError(f"classified_data должен быть словарём")
        if len(classified_data) == 0:
            logger.warning("Передан пустой словарь")
            return

        categories = classified_data.values()

        self.make_dirs(categories)

        errors = 0

        logger.info(f"Началось распределение писем по папкам в '{self.output_dir}'")
        for file_path, category in classified_data.items():
            try:
                self.distribute(file_path, category)
            except Exception as e:
                logger.warning(str(e))
                errors+=1

        if errors:
            logger.info(f"Распределение файлов по папкам завершено, не удалось переместить {errors} писем")
        else:
            logger.info(f"Распределение файлов по папкам успешно завершено")

    def distribute(self, file_path, category):
        if not file_path.exists():
            raise FileNotFoundError(f"Файл '{file_path}' не найден")

        new_file_path = self.output_dir / category / file_path.name

        if new_file_path.exists():
            raise FileExistsError(f"В '{category}' уже существует файл '{new_file_path}'")

        file_path.rename(new_file_path)
        logger.info(f"Файл '{file_path}' успешно перемещен в '{category}'")


    def make_dirs(self, categories):
        for category in categories:
            dir_path = self.output_dir / category

            if dir_path.exists():
                logger.info(f"Папка '{category}' уже существует")
                continue

            try:
                dir_path.mkdir(parents=True)
                logger.info(f"Папка '{category}' создана")
            except Exception as e:
                logger.exception(f"Не удалось создать папку '{category}': {e}")
                raise