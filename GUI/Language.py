class Language:
    AUDIO_EM = []
    IMG_EM = []
    BTNS_TEXTs = []
    DATA_TYPES = []
    LBL_TEXTs = []
    RT_DATA_TYPES = []
    CHECKBOX_TEXTs = []
    SYSTEM_MESS_GOOD = []
    SYSTEM_MESS_TMP = []
    SYSTEM_MESS_ERR = []
    WINDOW_NAMES = []


class LanguageUA (Language):
    def __init__(self):
        self.NAME = ['UA', 'EN']
        self.AUDIO_EM = ["Злість", "Спокій", "Огида", "Страх", "Щастя", "Нейтрально", "Сум", "Здивування"]
        self.IMG_EM = ["Злість", "Огида", "Страх", "Щастя", "Нейтрально", "Сум", "Здивування"]
        self.BTNS_TEXTs = ["ОБРОБИТИ", "ОБРАТИ ФАЙЛ", "ВИЙТИ", "НАЗАД", "ВІДТВОРИТИ ЗНОВУ"]
        self.DATA_TYPES = ["Відео зі звуком", "Лише відео без звуку", "З відео лише звук", "Лише звук", "Зображення"]
        self.LBL_TEXTs = ["Обраний файл: "]
        self.RT_DATA_TYPES = ["Відео зі звуком", "Лише відео без звуку", "Лише звук"]
        self.CHECKBOX_TEXTs = ["В режимі реального часу", "Зберегти до файлу", "Показати повний результат"]
        self.SYSTEM_MESS_GOOD = ["Готово!"]
        self.SYSTEM_MESS_TMP = ['Перевірка файлів...', "Йде обробка...",'Запуск пристроїв...', ' обробки при довжині ']
        self.SYSTEM_MESS_ERR = ["Щось пішло не так при обробці (", "Обраний файл не підходить до обраного формату", "Щось пішло не так(", "Щось не так з веб-камерою!", "Щось не так з мікрофоном!"]
        self.WINDOW_NAMES = ["Головне меню", "Обробка", "Вибір медіа-файлу"]


class LanguageEN (Language):
    def __init__(self):
        self.NAME = ['EN', 'UA']
        self.AUDIO_EM = ['Angry', 'Calm', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
        self.IMG_EM = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
        self.BTNS_TEXTs = ["START", "SELECT FILE", "EXIT", "GO BACK", "PLAY AGAIN"]
        self.DATA_TYPES = ["Video & sound", "Only video no sound", "Only sound from video", "Only sound", "Image"]
        self.LBL_TEXTs = ["Selected file: "]
        self.RT_DATA_TYPES = ["Video & sound", "Only video no sound", "Only sound"]
        self.CHECKBOX_TEXTs = ["In real time", "Save result to file", "Show full result"]
        self.SYSTEM_MESS_GOOD = ["Done!"]
        self.SYSTEM_MESS_TMP = ["Inspect Files...", "Processing...", "Starting web & mic...", ' for processing while len is ']
        self.SYSTEM_MESS_ERR = ["Something went wrong while processing (", "Wrong file for selected format!", "Something went wrong ("]
        self.WINDOW_NAMES = ["Main menu", "Processing", "Media-file selection"]


class LENG:
    elem = Language()

    @staticmethod
    def __init__():
        LENG.elem = LanguageUA()

    @staticmethod
    def change_language(res):
        tmp = {"EN": LanguageEN(), "UA": LanguageUA()}
        if res in tmp:
            LENG.elem = tmp[res]
        else:
            LENG.elem = LanguageUA()
