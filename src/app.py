import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.title("Настройка параметров обработки почты")
        self.geometry("700x450")



        paths_frame = ctk.CTkFrame(self)
        paths_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(paths_frame, text="Пути", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)

        self.rules_edit  = self._path_row(paths_frame, "Файл правил (.json):", str(config.rules_path))
        self.inbox_edit  = self._path_row(paths_frame, "Папка с письмами:", str(config.inbox_path))
        self.logs_edit   = self._path_row(paths_frame, "Папка для логов:", str(config.logs_output_path))
        self.report_edit = self._path_row(paths_frame, "Папка для отчётов:", str(config.report_path))
        self.output_edit = self._path_row(paths_frame, "Папка для писем:", str(config.classified_emails_path))



        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(settings_frame, text="Настройки", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)

        row = ctk.CTkFrame(settings_frame)
        row.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(row, text="Вес темы:").pack(side="left", padx=5)
        self.sub_entry = ctk.CTkEntry(row, width=50)
        self.sub_entry.insert(0, str(config.subject_points))
        self.sub_entry.pack(side="left", padx=5)

        ctk.CTkLabel(row, text="Вес текста:").pack(side="left", padx=5)
        self.text_entry = ctk.CTkEntry(row, width=50)
        self.text_entry.insert(0, str(config.text_points))
        self.text_entry.pack(side="left", padx=5)

        ctk.CTkLabel(row, text="Тип диаграммы:").pack(side="left", padx=5)
        self.chart_combo = ctk.CTkComboBox(row, values=["bar", "pie"], width=80)
        self.chart_combo.set(config.chart_type)
        self.chart_combo.pack(side="left", padx=5)


        self.apply_button = ctk.CTkButton(
            self, text="Применить",
            command=self.apply, height=40, font=("Arial", 14)
        )
        self.apply_button.pack(padx=20, pady=15, fill="x")

    def _path_row(self, parent, label: str, default: str) -> ctk.CTkEntry:
        row = ctk.CTkFrame(parent)
        row.pack(fill="x", padx=10, pady=3)
        ctk.CTkLabel(row, text=label, width=220, anchor="w").pack(side="left")
        edit = ctk.CTkEntry(row, width=320)
        edit.insert(0, default)
        edit.pack(side="left", padx=5)
        ctk.CTkButton(row, text="...", width=30,
                      command=lambda: self._browse(edit)).pack(side="left")
        return edit

    def _browse(self, edit: ctk.CTkEntry):
        path = filedialog.askdirectory(title="Выберите папку")
        if path:
            edit.delete(0, "end")
            edit.insert(0, path)

    def apply(self):
        try:
            sub = int(self.sub_entry.get())
            text = int(self.text_entry.get())
        except ValueError:
            ctk.CTkLabel(self, text= "Вес должен быть числом", text_color="red").pack()
            return

        self.config.set_by_user(
            rules_path=Path(self.rules_edit.get()),
            inbox_path=Path(self.inbox_edit.get()),
            logs_output_path=Path(self.logs_edit.get()),
            report_path=Path(self.report_edit.get()),
            classified_emails_path=Path(self.output_edit.get()),
            subject_points=sub,
            text_points=text,
            chart_type=self.chart_combo.get(),
        )
        self.destroy()  


def run_gui(config):
    app = MainWindow(config)
    app.mainloop()
