import time
from environs import Env
from datetime import datetime
from re import search

# environs use library
env = Env()
env.read_env()

# .env file read
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
BASIC_API = env.str("BASIC_API")
FORM_LINK_APP = env.str("FORM_LINK_APP")
FORM_LINK_SUBS = env.str("FORM_LINK_SUBS")
FORM_LINK_SHTAB = env.str("FORM_LINK_SHTAB")
FORM_LINK_EMPLOY = env.str("FORM_LINK_EMPLOY")
FORM_LINK_YMMT = env.str("FORM_LINK_YMMT")
FORM_LINK_MONO = env.str("FORM_LINK_MONO")
FORM_LINK_NNT = env.str("FORM_LINK_NNT")
FORM_LINK_ACT = env.str("FORM_LINK_ACT")

PAGES = env.str("PAGES")
TABLE_EMP = env.str("TABLE_EMP")

DOC_URL = env.str("DOC_URL")

UNKNOWN_MESSAGE = {
    "ўз": "Илтимос ноўрин хабар юборманг!",
    "ру": "Пожалуйста, не отправляйте неуместные сообщения",
    "uz": "Iltimos noo'rin xabar yubormang",
    "qq": "Ótinish orınsız xabar jibermang"
}
LANGS = ['ўз', 'ру', 'uz', 'qq']

SHARE_CONTACT_BUTTON = {
    "ўз": "☎️ Телефон рақам юбориш",
    "ру": "☎️ Отправить номер телефона",
    "uz": "☎️ Telefon raqam yuborish",
    "qq": "☎️ Telefon nomer jiberiw"
}
start_HELLO = {
    "ўз": "Ассалому алайкум Online-Mahalla телеграм ботига хуш келибсиз. "
          "Илтимос, телефон рақамингизни юборинг.",
    "ру": "Здравствуйте и добро пожаловать в телеграм-бот Online-Mahalla. "
          "Пожалуйста, пришлите свой номер телефона",
    "uz": "Assalomu alaykum Online-Mahalla telegram botiga xush kelibsiz. "
          "Iltimos, telefon raqamingizni yuboring",
    "qq": "Assalawma aleykum Online-Mahalla telegram botiga xosh kelipsiz. "
          "Ótinish, telefon nomerińizdi jiberiń."
}
CREATE_APPEAL = {
    "ўз": "📝 Мурожаат юбориш",
    "ру": "📝 Отправить обращение",
    "uz": "📝 Murojaat yuborish",
    "qq": "📝 Shaqırıq jiberiw"
}
CREATE_APPEAL_SHTAB = {
    "ўз": "📜 Штабга мурожаат",
    "ру": "📜 Обращение в штаб",
    "uz": "📜 Shtabga murojaat",
    "qq": "📜 Shtabga shaqırıq "
}
APPEALS = {
    "ўз": "Мурожаатларингиз:",
    "ру": "Ваши обращение:",
    "uz": "Murojaatlaringiz:",
    "qq": "Shaqırıwlarıńız:"
}
SHARE_CONTACT_MESSAGE = {
    "ўз": "Қабул қилинди",
    "ру": "Принято",
    "uz": "Qabul qilindi",
    "qq": "Qabıllandı"
}
EMPTY_APPS_LIST = {
    "ўз": "Мурожаатларингиз мавжуд эмас",
    "ру": "Ваши обращения недоступны",
    "uz": "Murojaatlaringiz mavjud emas",
    "qq": "Shaqırıwlarıńız joq "
}
NOT_OWN_NUMBER = {
    "ўз": "Ушбу рақам телеграмингизга боғланган эмас!\nИлтимос, пастдаги тугма орқали рақамингизни юборинг.",
    "ру": "Этот номер не привязан к вашему телеграмму!\nПожалуйста, отправьте свой номер с помощью кнопки ниже.",
    "uz": "Ushbu raqam telegramingizga bog'langan emas!\nIltimos, pastdagi tugma orqali raqamingizni yuboring.",
    "qq": "Bul nomer telegramingizga baylanısqan emes!\nÓtinish, tómendegi tuyme arqalı nomerińizdi jiberiń."
}
VIEW_DOC = {
    "ўз": "🌐  Ҳужжатни кўриш",
    "ру": "🌐  Посмотреть документ",
    "uz": "🌐  Hujjatni ko'rish",
    "qq": "🌐  Hújjetti kóriw"
}
MAIN_APPEAL = {
    "ўз": "📨 Мурожаатлар",
    "ру": "📨 Обращение",
    "uz": "📨 Murojaatlar",
    "qq": "📨 Shaqırıqlar"
}
MAIN_SUBSIDY = {
    "ўз": "💰 Субсидиялар",
    "ру": "💰 Субсидии",
    "uz": "💰 Subsidiyalar",
    "qq": "💰 Subsidiyalar"
}
MAIN_EMPLOYMENT = {
    "ўз": "💼 Ишга жойлаштириш",
    "ру": "💼 Трудоустройство",
    "uz": "💼 Ishga joylashtirish",
    "qq": "💼 Jumısqa jaylastırıw"
}
MAIN_REFERRAL = {
    "ўз": "🎓 Ўқишга йўналтириш",
    "ру": "🎓 Направление на учебу",
    "uz": "🎓 O'qishga yo'naltirish",
    "qq": "🎓 Oqıwǵa jóneltiriw"
}
MAIN_BUSINESES = {
    "ўз": "👨‍💼 Тадбиркорлар",
    "ру": "👨‍💼 Предприниматели",
    "uz": "👨‍💼 Tadbirkorlar",
    "qq": "👨‍💼 Isbilermenler"
}
MAIN_NOTEBOOKS = {
    "ўз": "📚 Дафтарлар",
    "ру": "📚 Ноутбуки",
    "uz": "📚 Daftarlar",
    "qq": "📚 Dápterler"
}
MAIN_ACTS = {
    "ўз": "📜 Далолатномалар",
    "ру": "📜 Акты",
    "uz": "📜 Dalolatnomalar",
    "qq": "📜 Aktlar"
}
MAIN_MANUAL = {
    "ўз": "🗒 Қўлланма.pdf",
    "ру": "🗒 Руководство.pdf",
    "uz": "🗒 Qo'llanma.pdf",
    "qq": "🗒 Qóllanba.pdf"
}
DOWN_NOTEBOOKS = {
    "ўз": "Дафтарлар рўйхатини юклаб олиш",
    "ру": "Скачать список блокнотов",
    "uz": "Daftarlar ro'yxatini yuklab olish",
    "qq": "Dápterler dizimin júklep alıw"
}
WOMEN = {
    "ўз": "📕 Аёллар дафтари",
    "ру": "📕 Женский блокнот",
    "uz": "📕 Ayollar daftari",
    "qq": "📕 Hayallar dápteri"
}
YOUNG = {
    "ўз": "📗 Ёшлар дафтари",
    "ру": "📗 Молодежный блокнот",
    "uz": "📗 Yoshlar daftari",
    "qq": "📗 Jaslar dápteri"
}
IRON = {
    "ўз": "📙 Темир дафтар",
    "ру": "📙 Железный блокнот",
    "uz": "📙 Temir daftar",
    "qq": "📙 Temir dápter"
}
SOCIAL_REGISTER = {
    "ўз": "📘 Ягона ижтимоий реестр",
    "ру": "📘 Единый социальный регистр",
    "uz": "📘 Yagona ijtimoiy reyestr",
    "qq": "📘 Birden-bir social reyestr"
}
UNEMPLOYED = {
    "ўз": "📒 Ишсизлар",
    "ру": "📒 Безработный",
    "uz": "📒 Ishsizlar",
    "qq": "📒 Jumıssızlar"
}
SUBS_APPL = {
    "ўз": "📝 Ариза юбориш",
    "ру": "📝 Подавать заявление",
    "uz": "📝 Ariza yuborish",
    "qq": "📝 Arza jiberiw"
}
SUBSIDIES = {
    "ўз": "Субсидияга юборилган аризаларингиз:",
    "ру": "Поданные заявки на получение субсидии:",
    "uz": "Subsidiyaga yuborilgan arizalaringiz:",
    "qq": "Subsidiyaga jiberilgen arzalarıńız:"
}
NOT_FOUND_SUBSIDIES = {
    "ўз": "Субсидияга аризаларингиз мавжуд эмас",
    "ру": "Ваши заявки на субсидию недоступны",
    "uz": "Subsidiyaga arizalaringiz mavjud emas",
    "qq": "Subsidiyaga arizalaringiz mavjud emas"
}
NOT_FOUND_URL = {
    "ўз": "Ҳужжат яратилмаган",
    "ру": "Документ не создан",
    "uz": "Hujjat yaratilmagan",
    "qq": "Hújjet jaratılmaǵan"
}
HOKIM_APPS = {
    "ўз": "📥 Маҳалла бўйича мурожаатлар",
    "ру": "📥 Обращение по районам",
    "uz": "📥 Mahalla bo'yicha murojaatlar",
    "qq": "📥 Máhelle boyınsha shaqırıwlar "
}
HOKIM_SUBS = {
    "ўз": "📥 Маҳалла бўйича субсидиялар",
    "ру": "📥 Субсидии по районам",
    "uz": "📥 Mahalla bo'yicha subsidiyalar",
    "qq": "📥 Máhelle boyınsha subsidiyalar"
}
RECIEVED_APPS = {
    "ўз": "та мурожаат келиб тушган",
    "ру": "обращение(я) получено",
    "uz": "ta murojaat kelib tushgan",
    "qq": "ta murojaat kelib tushgan"
}
RECIEVED_SUBS = {
    "ўз": "та ариза келиб тушган",
    "ру": "заявление(я) получено",
    "uz": "ta ariza kelib tushgan",
    "qq": "ta ariza kelib tushgan"
}
EMPLOY_INLINE = {
    "ўз": "Маълумотнома",
    "ру": "Ссылка",
    "uz": "Ma'lumotnoma",
    "qq": "Málimleme"
}
EMPLOY_INLINE_YMMT = {
    "ўз": "Йўлланма (ЯММТ)",
    "ру": "Направления (ЯММТ)",
    "uz": "Yo'llanma (YMMT)",
    "qq": "Jollanba (YMMT)"
}
REF_INLINE_MONO = {
    "ўз": "Мономарказга",
    "ру": "К Моноцентру",
    "uz": "Monomarkazga",
    "qq": "Monomarkazga"
}
REF_INLINE_NNT = {
    "ўз": "НТТ/ННТ га",
    "ру": "К НТТ/ННТ",
    "uz": "NTT/NNT ga",
    "qq": "NTT/NNT ga"
}
GOTO_SITE_REFER = {
    "ўз": "Ўқишга йўналтирилганлар рўйхати",
    "ру": "Список учебных пособий",
    "uz": "O'qishga yo'naltirilganlar ro'yxati",
    "qq": "Oqıwǵa jóneltirilganlar dizimi"
}
THESE_TEXT_EMP = {
    "ўз": "Ишга жойлаштириш тури",
    "ру": "Тип занятости",
    "uz": "Ishga joylashtirish turi",
    "qq": "Jumısqa jaylastırıw túri"
}
THESE_TEXT_REF = {
    "ўз": "Ўқишга йўналтириш тури",
    "ру": "Тип направления на исследование",
    "uz": "O'qishga yo'naltirish turi",
    "qq": "Oqıwǵa jóneltiriw túri"
}
GOTO_SITE_EMPLOY = {
    "ўз": "Ишга жойлаштирилганлар рўйхати",
    "ру": "Список занятых лиц",
    "uz": "Ishga joylashtirilganlar ro'yxati",
    "qq": "Jumısqa jaylastırilganlar dizimi"
}
GOTO_SITE_APP = {
    "ўз": "Мурожаатлар рўйхати",
    "ру": "Список обрашение",
    "uz": "Murojaatlar ro'yxati",
    "qq": "Shaqırıwlar dizimi"
}
GOTO_SITE_SUBS = {
    "ўз": "Субсидиялар рўйхати",
    "ру": "Список субсидий",
    "uz": "Subsidiyalar ro'yxati",
    "qq": "Subsidiyalar dizimi"
}
TEXT_MANY_INFO = {
    "ўз": "Маълумот кўплиги сабабли платформадан кўришни тавсия қиламиз",
    "ру": "Рекомендуем смотреть с платформы из-за обилия информации",
    "uz": "Ma'lumot ko'pligi sababli platformadan ko'rishni tavsiya qilamiz",
    "qq": "Maǵlıwmat kópligi sebepli platformadan kóriwdi usınıs etemiz"
}
NOT_FOUND_APPS = {
    "ўз": "Бирорта ҳам мурожаат топилмади",
    "ру": "Ссылки не найдены",
    "uz": "Birorta ham murojaat topilmadi",
    "qq": "Qandayda-bir de shaqırıq tabilǵan zatdı"
}
NOT_FOUND_INFO = {
    "ўз": "Бирорта ҳам маълумот топилмади",
    "ру": "Информация не найдена",
    "uz": "Birorta ham ma'lumot topilmadi",
    "qq": "Qandayda-bir de maǵlıwmat tabilǵan zatdı"
}
TEXT_WOMEN = {
    "ўз": "Маҳалла бўйича Аёллар дафтарига киритилганлар рўйхати:",
    "ру": "Список записей в Женском реестре по районам:",
    "uz": "Mahalla bo'yicha Ayollar daftariga kiritilganlar ro'yxati:",
    "qq": "Máhelle boyınsha Hayallar dápterine kiritilgenler dizimi:"
}
TEXT_YOUNG = {
    "ўз": "Маҳалла бўйича Ёшлар дафтарига киритилганлар рўйхати:",
    "ру": "Список включенных в Реестр молодежи по районам:",
    "uz": "Mahalla bo'yicha Yoshlar daftariga kiritilganlar ro'yxati:",
    "qq": "Máhelle boyınsha Jaslar dápterine kiritilgenler dizimi:"
}
TEXT_IRON = {
    "ўз": "Маҳалла бўйича Темир дафтарга киритилганлар рўйхати:",
    "ру": "Список включенных в Железный реестр по районам:",
    "uz": "Mahalla bo'yicha Temir daftarga kiritilganlar ro'yxati:",
    "qq": "Máhelle boyınsha Temir dápterge kiritilgenler dizimi:"
}
TEXT_BUS = {
    "ўз": "Маҳалла бўйича тадбиркорлик субектлари:",
    "ру": "Субъекты хозяйствования по районам:",
    "uz": "Mahalla bo'yicha tadbirkorlik subyektlari:",
    "qq": "Máhelle boyınsha isbilermenlik subektleri:"
}
TEXT_SOCIAL = {
    "ўз": "Маҳалла бўйича ягона ижтимоий реестр рўйхати:",
    "ру": "Единый список социальных регистров по районам:",
    "uz": "Mahalla bo'yicha yagona ijtimoiy reyestr ro'yxati:",
    "qq": "Máhelle boyınsha birden-bir social reyestr dizimi:"
}
TEXT_UNEMP = {
    "ўз": "Маҳалла бўйича расман ишсизлар рўйхати:",
    "ру": "Список официально безработных по районам:",
    "uz": "Mahalla bo'yicha rasman ishsizlar ro'yxati:",
    "qq": "Máhelle boyınsha rásmiy jumıssızlar dizimi:"
}
ADD_ACT = {
    "ўз": "➕ Далолатнома қўшиш",
    "ру": "➕ Добавление акта",
    "uz": "➕ Dalolatnoma qo'shish",
    "qq": "➕ Akt qosıw"
}
VIEW_ACTS = {
    "ўз": "🌐  Маҳалла бўйича далолатномалар",
    "ру": "🌐  Акти по районам",
    "uz": "🌐  Mahalla bo'yicha dalolatnomalar",
    "qq": "🌐  Máhelle boyınsha aktlar"
}
UNIT_ACTS = {
    "ўз": "Далолатномалар бўлими",
    "ру": "Отделение акти",
    "uz": "Dalolatnomalar bo'limi",
    "qq": "Aktlar bólimi"
}

btn_langs = (
        ('Ўзбекча', 'ўз'),
        ('Русский', 'ру'),
        ('O`zbekcha', 'uz'),
        ('Qaraqalpaqsha ', 'qq')
    )

open_document = lambda doc_guid, doc_pin: f"https://hujjat.uz/document?id={doc_guid}&pin={doc_pin}"

get_id = lambda id: '' if id == None else f'№ {id}'

def get_icon(doc_status: str):
    if doc_status == 'FULL_SIGNED': return '✅'
    elif doc_status == 'CREATED': return '❓'
    elif doc_status == 'CANCELED': return '❌'
    elif doc_status == None: return '❓'
    elif search('REJECTED', doc_status): return '🚫'
    elif search('AT_', doc_status): return '🕥'
    elif search('IN_', doc_status): return '🕥'
    else: return '✅'

def get_date(date):
    if date == None: return ''
    else:
        d = datetime.strptime(date, '%Y-%m-%d')
        return f"{d.strftime('%d.%m.%Y')} даги"

lines_count = 0
def clear_logs():
    global lines_count
    lines_count += 1
    if lines_count == 10000:
        with open('logs.txt', 'w') as file:
            file.write(f'cleared at {time.asctime()}\n')