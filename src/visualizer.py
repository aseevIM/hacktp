import matplotlib.pyplot as plt
from pathlib import Path

import logging
logger = logging.getLogger("processor")

class Visualizer:
    def __init__(self, classified_data):
        self.analytics = self.get_analytics(classified_data)

    # Переводит полученные данные в список категорий и количество каждой: Категория -> Кол-во писем
    def get_analytics(self, classified_data):
        if type(classified_data) != dict:
            logger.error(f"classified_data должна быть словарем, получен '{type(classified_data)}'")
            raise TypeError(f"classified_data должна быть словарем, получен '{type(classified_data)}'")
        if not classified_data:
            logger.warning("Пустые входные данные")
            return {}


        analytics = {}
        categories = list(classified_data.values())

        for category in categories:
            analytics[category] = categories.count(category)

        return analytics

    # Возвращает диаграмму, выбранную пользователем
    def get_schedule(self, prefer_table):
        categories = list(self.analytics.keys())
        values = list(self.analytics.values())

        try:
            if prefer_table == "bar":
                table = self.build_bar(categories, values)
            elif prefer_table == "pie":
                table = self.build_pie(categories, values)
            else:
                logger.error(f"Выбран неизвестный тип диаграммы: '{self.prefer_table}'")
                return None

            logger.info("Диаграмма создана")
            return table

        except Exception:
            logger.exception("Не удалось построить диаграмму")
            return None

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
        axes.pie(values, labels=categories)

        # настройка заголовка диаграммы
        axes.set_title("Количество писем")

        # Возвращаем фигуру чтобы можно было сохранить в pdf/png
        return fig

    def show_table(self, prefer_table):
        table = self.get_schedule(prefer_table)
        if table is None:
            logger.warning("Диаграмма не была создана")
            return
        else:
            plt.show()

    def save_to_html(self, output_dir, prefer_table):
        # получение диаграммы
        try:
            fig = self.get_schedule(prefer_table)
            if fig is None:
                logger.error("диаграмма не была создана, статистика не сохранится")
                return

            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # пути до файла и картинки
            img_path = output_dir / "chart.png"
            output_path = output_dir / "report.html"


            fig.savefig(img_path)
            plt.close(fig)


            # Визуал html сделал через генеративную нейросеть
            total = sum(self.analytics.values())
            rows = ""
            for category, count in self.analytics.items():
                percent = count / total * 100
                rows += f"""
                    <tr>
                        <td>{category}</td>
                        <td>{count}</td>
                        <td>{percent:.1f}%</td>
                    </tr>"""

            html = f"""
                <!DOCTYPE html>
                <html lang="ru">
                <head>
                    <meta charset="UTF-8">
                    <title>Отчёт по обработке почты</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            max-width: 800px;
                            margin: 40px auto;
                            background: #f5f5f5;
                            color: #333;
                        }}
                        h1 {{
                            color: #2c3e50;
                            border-bottom: 2px solid #3498db;
                            padding-bottom: 10px;
                        }}
                        .summary {{
                            background: #3498db;
                            color: white;
                            padding: 15px 20px;
                            border-radius: 8px;
                            font-size: 18px;
                            margin-bottom: 30px;
                        }}
                        table {{
                            width: 100%;
                            border-collapse: collapse;
                            background: white;
                            border-radius: 8px;
                            overflow: hidden;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                            margin-bottom: 30px;
                        }}
                        th {{
                            background: #2c3e50;
                            color: white;
                            padding: 12px 16px;
                            text-align: left;
                        }}
                        td {{
                            padding: 10px 16px;
                            border-bottom: 1px solid #eee;
                        }}
                        tr:last-child td {{
                            border-bottom: none;
                            font-weight: bold;
                            background: #ecf0f1;
                        }}
                        img {{
                            width: 100%;
                            border-radius: 8px;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        }}
                    </style>
                </head>
                <body>
                    <h1>Отчёт по обработке почты</h1>
    
                    <div class="summary">
                        Всего писем обработано: {total}
                    </div>
    
                    <h2>Статистика по категориям</h2>
                    <table>
                        <tr>
                            <th>Категория</th>
                            <th>Количество</th>
                            <th>Процент</th>
                        </tr>
                        {rows}
                        <tr>
                            <td>Итого</td>
                            <td>{total}</td>
                            <td>100%</td>
                        </tr>
                    </table>
    
                    <h2>Диаграмма</h2>
                    <img src="chart.png" alt="Диаграмма по категориям"/>
    
                </body>
                </html>
                """

            output_path.write_text(html, encoding="utf-8")
            logger.info(f"HTML отчёт сохранён: {output_path}")
            return output_path

        except Exception as e:
            logger.error("Ошибка при создании HTML отчёта")
            return None


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
        "mail7.eml": "spam",
        "mail8.eml": "incidents",
        "mail9.eml": "incidents",
        "mail10.eml": "important",
        "mail11.eml": "important",
        "mail12.eml": "requests",
        "mail13.eml": "spam",
        "mail14.eml": "other",
        "mail15.eml": "requests",
        "mail16.eml": "auto_notifications",
        "mail17.eml": "auto_notifications",
        "mail18.eml": "auto_notifications",
        "mail19.eml": "important",
        "mail20.eml": "incidents",
        "mail21.eml": "spam",
        "mail22.eml": "requests",
        "mail23.eml": "unknown",
        "mail24.eml": "unknown",
        "mail25.eml": "important",
    }


    viz = Visualizer(test_data)
    #viz.show_table("bar")
    viz.show_table("pie")
    viz.save_to_html(Path("test_report"), "bar")

    # Работает как bar, так и pie
    # Можете проверить у себя
    # Я потом перенесу в тесты



