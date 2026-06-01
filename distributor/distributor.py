class Distributor:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def distribute_all(self, classified_data):
        file_paths = classified_data.keys()
        categories = classified_data.values()

        self.make_dirs(categories)

        for file_path in file_paths:
            self.distribute(file_path, categories)

    def distribute(self, file_path, category):
        new_file_path = self.output_dir / category / file_path.name

        if new_file_path.exists(): return

        file_path.rename(new_file_path)

    def make_dirs(self, categories):
        for category in categories:
            dir_path = self.output_dir / category

            if dir_path.exists(): continue

            dir_path.mkdir()