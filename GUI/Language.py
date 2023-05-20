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
        self.AUDIO_EM = ["Нейтрально", "Спокій", "Щастя", "Сум", "Злість", "Переляк", "Огида", "Здивування"]
        self.IMG_EM = ["Злість", "Огида", "Страх", "Щастя", "Cум", "Здивування", "Нейтрально"]
        self.BTNS_TEXTs = ["ОБРОБИТИ", "ОБРАТИ ФАЙЛ", "ВИЙТИ", "НАЗАД"]
        self.DATA_TYPES = ["Відео зі звуком", "Лише відео без звуку", "З відео лише звук", "Лише звук", "Зображення"]
        self.LBL_TEXTs = ["Обраний файл: "]
        self.RT_DATA_TYPES = ["Відео зі звуком", "Лише відео без звуку", "З відео лише звук", "Лише звук"]
        self.CHECKBOX_TEXTs = ["В режимі реального часу", "Зберегти до файлу", "Показати повний результат"]
        self.SYSTEM_MESS_GOOD = ["Готово!"]
        self.SYSTEM_MESS_TMP = ['Перевірка файлів...', "Йде обробка...",'Запуск пристроїв...']
        self.SYSTEM_MESS_ERR = ["Щось пішло не так при обробці (", "Обраний файл не підходить до обраного формату", "Щось пішло не так("]
        self.WINDOW_NAMES = ["Головне меню", "Обробка"]


class LanguageEN (Language):
    def __init__(self):
        self.AUDIO_EM = ['Neutral', 'Calm', 'Happy', 'Sad', 'Angry', 'Fear', 'Disgust', 'Surprise']
        self.IMG_EM = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        self.BTNS_TEXTs = ["START", "SELECT FILE", "EXIT", "GO BACK"]
        self.DATA_TYPES = ["Video & sound", "Only video no sound", "Only sound from video", "Only sound", "Image"]
        self.LBL_TEXTs = ["Selected file: "]
        self.RT_DATA_TYPES = ["Video & sound", "Only video no sound", "Only sound from video", "Only sound"]
        self.CHECKBOX_TEXTs = ["In real time", "Save result to file", "Show full result"]
        self.SYSTEM_MESS_GOOD = ["Done!"]
        self.SYSTEM_MESS_TMP = ["Inspect Files...", "Processing...", "Starting web & mic..."]
        self.SYSTEM_MESS_ERR = ["Something went wrong while processing (", "Wrong file for selected format!", "Something went wrong ("]
        self.WINDOW_NAMES = ["Main menu", "Processing"]


class LENG:
    elem = Language()
    LANG_LIST = ["UA", "EN"]

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
