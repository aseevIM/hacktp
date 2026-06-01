# проверяем наличие inbox
if [ ! -d "./inbox" ]; then
    echo "ОШИБКА: Папка ./inbox не найдена"
    exit 1
fi

if [ -z "$(ls -A ./inbox 2>/dev/null)" ]; then
    echo "ПРЕДУПРЕЖДЕНИЕ: Папка ./inbox пуста"
    exit 1
fi

#проверяем наличие питона, ну на всякий
if ! command -v python3 &> /dev/null; then
    echo "ОШИБКА: Python 3 не установлен"
    exit 1
fi

# смотрим pip
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "ОШИБКА: pip не установлен"
    exit 1
fi

# проверка установленных библиотек
NEED_INSTALL=0

if ! python3 -c "import matplotlib" &> /dev/null; then
    NEED_INSTALL=1
fi

if ! python3 -c "import seaborn" &> /dev/null; then
    NEED_INSTALL=1
fi

if ! python3 -c "import pytest" &> /dev/null; then
    NEED_INSTALL=1
fi

if [ $NEED_INSTALL -eq 1 ]; then
    $PIP_CMD install matplotlib seaborn pytest -q
fi

# запускаем приложуху
python3 src/main.py --inbox ./inbox --output ./sorted "$@"

exit $?
