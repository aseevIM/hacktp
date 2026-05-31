import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self, classified_data, output_dir, prefer_table):
        self.analytics = self.get_analytics(classified_data)
        self.output_dir = output_dir
        self.prefer_table = prefer_table

    # Переводит полученные данные в список категорий и количество каждой: Категория -> Кол-во писем
    def get_analytics(self, classified_data):
        analytics = {}
        categories = list(classified_data.values())

        for category in categories:
            analytics[category] = categories.count(category)

        return analytics

    # озвращает диаграмму, выбранную пользователем
    def get_schedule(self):
        categories = list(self.analytics.keys())
        values = list(self.analytics.values())

        if self.prefer_table == "bar":
            table = self.build_bar(categories, values)
        elif self.prefer_table == "pie":
            table = self.build_pie(categories, values)
        else:
            # !!!! Добавить логгер
            print(f"Выбран неизвестный тип диаграммы: '{self.prefer_table}'. Необходимо выбрать bar или pie")
            return None

        # Для проверки
        plt.show()

        return table

    # Строит столбчатую диаграмму
    def build_bar(self, categories, values):
        fig, axes = plt.subplots()
        axes.bar(categories, values)

        # настройка подписей на осях
        axes.set_title("Количество писем")
        axes.set_xlabel("Категория")
        axes.set_ylabel("Количество")

        # Возвращаем фигуру чтобы можно было сохранить в pdf/png
        return fig

    # Строит круговую диаграмму
    def build_pie(self, categories, values):
        fig, axes = plt.subplots()
        axes.pie(x=values, labels=categories)

        # настройка заголовка диаграммы
        axes.set_title("Количество писем")

        # Возвращаем фигуру чтобы можно было сохранить в pdf/png
        return fig


# Тестовый набор для проверки работоспособности
# !!!! Удалить
if __name__ == "__main__":
    test_data = {
        "mail1.eml": "spam",
        "mail2.eml": "spam",
        "mail3.eml": "incidents",
        "mail4.eml": "requests",
        "mail5.eml": "spam",
        "mail6.eml": "other",
    }


    viz = Visualizer(test_data, "logs", "bar")
    viz.get_schedule()

    # Работает как ber, так и pie
    # Можете проверить у себя



