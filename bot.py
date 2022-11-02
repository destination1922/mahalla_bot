import os
import logging
import asyncio
import threading
from config import *
from write_excel import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo

logging.basicConfig(
    filename='logs.txt',
    filemode='a',
    level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def command_start(query: types.CallbackQuery):
    clear_logs()
    telegram_id = query.from_user.id
    first_name = query.from_user.first_name
    logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, command: start")

    keyboard_markup = types.InlineKeyboardMarkup(row_width=4)
    row_btn4 = (types.InlineKeyboardButton(text, callback_data=data) for text, data in btn_langs)
    keyboard_markup.add(*row_btn4)
    await bot.send_message(telegram_id, text='Тилни танланг', reply_markup=keyboard_markup)

@dp.callback_query_handler()
async def callback_function(query: types.CallbackQuery):
    clear_logs()
    telegram_id = query.from_user.id
    first_name = query.from_user.first_name
    query_text = query.data

    r = requests.get(f"{BASIC_API}lang_get?telegram_id={telegram_id}")
    lang_data = r.json()
    lang = lang_data['data']

    r_phone_data = requests.get(f"{BASIC_API}get_phone?telegram_id={telegram_id}")
    phone_data = r_phone_data.json()
    phone = phone_data['data']['phone_number']

    r_user_info = requests.get(f"{BASIC_API}get_user_info?phone={phone}")
    user_info = r_user_info.json()
    user_data = user_info['data']

    if query_text in LANGS:
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, Selected lang ")
        lang = query_text
        requests.post(f"{BASIC_API}lang_post?telegram_id={telegram_id}&lang={lang}")
        contact_btn = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True,
            keyboard=[
                [
                    types.KeyboardButton(text=SHARE_CONTACT_BUTTON[lang], request_contact=True)
                ]
            ]
        )
        await bot.send_message(chat_id=telegram_id, text=start_HELLO[lang], reply_markup=contact_btn)

    elif query_text == 'url_not_found':
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, Url not found")
        await query.answer(text=NOT_FOUND_URL[lang])

    elif query_text == 'hokim_apps':
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, Hokim appeals")
        dapps_array = []
        dapps_array_null = []

        r_by_dist = requests.get(f"{BASIC_API}get_by_dist?district_id={user_data['district_id']}")
        by_dist_data = r_by_dist.json()
        dist_data = by_dist_data['data']
        if dist_data:
            emp_link = types.InlineKeyboardButton(
                        text='🌐  ' + GOTO_SITE_APP[lang],
                        url=f"{PAGES}appeals?obl_id={user_data['obl_id']}&"
                            f"area_id={user_data['area_id']}&district_id={user_data['district_id']}")
            if len(dist_data) < 31:
                for app_id in dist_data:
                    ar_i = []
                    i = app_id['id']
                    r_app = requests.get(f"{BASIC_API}get_appeal?id={i}")
                    app_data = r_app.json()
                    data = app_data['data']
                    if data['doc_guid'] and data['doc_pin']:
                        text_app_id = f"🌐  {get_date(app_id['created_at'])}  {get_id(i)}  {app_id['fullname']}"
                        ar_i.append(text_app_id)
                        ar_i.append(open_document(data['doc_guid'], data['doc_pin']))
                        dapps_array.append(ar_i)
                    else:
                        text_app_id = get_date(app_id['created_at']) + '  ' + get_id(i) + '  ' + app_id['fullname']
                        ar_i.append(text_app_id)
                        ar_i.append('url_not_found')
                        dapps_array_null.append(ar_i)
                btn_apps = (types.InlineKeyboardButton(text, url=url) for text, url in dapps_array)
                btn_apps_null = (types.InlineKeyboardButton(text, callback_data=data) for text, data in
                                 dapps_array_null)
                app_count = len(dapps_array) + len(dapps_array_null)
                keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
                keyboard_markup.add(*btn_apps)
                keyboard_markup.add(*btn_apps_null)
                keyboard_markup.add(emp_link)
                await bot.send_message(chat_id=telegram_id,
                                       text=f'{app_count} {RECIEVED_APPS[lang]}',
                                       reply_markup=keyboard_markup)
            else:
                btn_emp_link = types.InlineKeyboardMarkup().add(emp_link)
                await bot.send_message(chat_id=telegram_id,text=TEXT_MANY_INFO[lang], reply_markup=btn_emp_link)
        else:
            await query.answer(text=NOT_FOUND_APPS[lang])

    elif query_text == 'hokim_subs':
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, Hokim subsidies")
        subs_array = []
        subs_array_null = []

        r_by_dist = requests.get(f"{BASIC_API}get_subs_by_dist?mahalla_id={user_data['district_id']}")
        by_dist_data = r_by_dist.json()
        dist_data = by_dist_data['data']
        if dist_data:
            sub_link = types.InlineKeyboardButton(
                            text='🌐  ' + GOTO_SITE_SUBS[lang],
                            url=f"{PAGES}subsidy_assistance_inner?obl_id={user_data['obl_id']}&"
                                f"area_id={user_data['area_id']}&district_id={user_data['district_id']}&tab=2")
            if len(dist_data) < 31:
                for sub_id in dist_data:
                    ar_i = []

                    i = sub_id['id']
                    r_app = requests.get(f"{BASIC_API}get_subs_by_id?sub_id={i}")
                    sub_data = r_app.json()
                    data = sub_data['data']
                    text_sub_id = f"{get_date(sub_id['created_at'])}  {get_id(i)}  " \
                                  f"{get_icon(sub_id['doc_status'])} {sub_id['sender_name']}"
                    ar_i.append(text_sub_id)
                    if data['doc_short_url']:
                        ar_i.append(data['doc_short_url'])
                        subs_array.append(ar_i)
                    else:
                        ar_i.append(f'url_not_found')
                        subs_array_null.append(ar_i)
                btn_subs = (types.InlineKeyboardButton(text, url=url) for text, url in subs_array)
                btn_subs_null = (types.InlineKeyboardButton(text, callback_data=data) for text, data in subs_array_null)
                subs_count = len(subs_array) + len(subs_array_null)
                keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
                keyboard_markup.add(*btn_subs)
                keyboard_markup.add(*btn_subs_null)
                keyboard_markup.add(sub_link)

                await bot.send_message(chat_id=telegram_id, text=f'{subs_count} {RECIEVED_SUBS[lang]}',
                                       reply_markup=keyboard_markup)
            else:
                btn_sub_link = types.InlineKeyboardMarkup().add(sub_link)
                await bot.send_message(chat_id=telegram_id, text=TEXT_MANY_INFO[lang], reply_markup=btn_sub_link)
        else:
            await query.answer(text=NOT_FOUND_INFO[lang])
    elif query_text == 'women':
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, women selected")
        await query.message.answer(text=TEXT_WOMEN[lang])
        at_time = excel_women('women', 'get_women', user_data['district_id'])
        await bot.send_document(chat_id=telegram_id, document=open(f'Аёллар дафтари{at_time}.xlsx', 'rb'))
        os.remove(f'Аёллар дафтари{at_time}.xlsx')

    elif query_text == 'young':
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, young selected")
        await query.message.answer(text=NOT_FOUND_INFO[lang])
        # at_time = excel_young('young', 'get_young', user_data['district_id'])
        # await bot.send_document(chat_id=telegram_id, document=open(f'Ёшлар дафтари{at_time}.xlsx', 'rb'))
        # os.remove(f'Ёшлар дафтари{at_time}.xlsx')

    elif query_text == 'iron':
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, iron selected")
        await query.message.answer(text=TEXT_IRON[lang])
        at_time = excel_iron('iron', 'get_iron', user_data['district_id'])
        await bot.send_document(chat_id=telegram_id, document=open(f'Темир дафтар{at_time}.xlsx', 'rb'))
        os.remove(f'Темир дафтар{at_time}.xlsx')

    elif query_text == 'social':
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, social register selected")
        await query.message.answer(text=TEXT_SOCIAL[lang])
        at_time = excel_social('social', 'get_social_reg', user_data['district_id'])
        await bot.send_document(chat_id=telegram_id, document=open(f'Ягона ижтимоий реестр{at_time}.xlsx', 'rb'))
        os.remove(f'Ягона ижтимоий реестр{at_time}.xlsx')

    elif query_text == 'unemp':
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, unemployed selected")
        await query.message.answer(text=NOT_FOUND_INFO[lang])
        # at_time = excel_unemp('unemp', 'get_unemp', user_data['district_id'])
        # await bot.send_document(chat_id=telegram_id, document=open(f'Расман ишсизлар{at_time}.xlsx', 'rb'))
        # os.remove(f'Расман ишсизлар{at_time}.xlsx')

    else:
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, Unkonwn error")

@dp.message_handler(content_types='contact')
async def get_contact(message: types.Message):
    clear_logs()
    phone = message.contact.phone_number
    telegram_id = message.from_user.id
    first_name = message.from_user.first_name
    logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, contact: {phone}")

    r = requests.get(f"{BASIC_API}lang_get?telegram_id={telegram_id}")
    data = r.json()
    lang = data['data']

    # Hokim yordamchisi
    r_user_info = requests.get(f"{BASIC_API}get_user_info?phone={phone}")
    user_info = r_user_info.json()
    user_data = user_info['data']

    if telegram_id == message.contact.user_id:
        requests.post(f"{BASIC_API}insert_user?telegram_id={telegram_id}&phone={phone}")
        main_btns = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn12 = (types.KeyboardButton(text=MAIN_APPEAL[lang]), types.KeyboardButton(text=MAIN_SUBSIDY[lang]))
        btn34 = (types.KeyboardButton(text=MAIN_EMPLOYMENT[lang]), types.KeyboardButton(text=MAIN_REFERRAL[lang]))

        main_btns.add(*btn12)
        main_btns.add(*btn34)
        if len(user_data) != 0 and user_data['level'] == 4 and user_data['org_type'] == 100:
            btn56 = (types.KeyboardButton(text=MAIN_BUSINESES[lang]),
                     types.KeyboardButton(text=MAIN_NOTEBOOKS[lang]))
            btn7 = (types.KeyboardButton(text=MAIN_MANUAL[lang]), types.KeyboardButton(text=MAIN_ACTS[lang]))
            main_btns.add(*btn56)
            main_btns.add(*btn7)
        else:
            btn7 = types.KeyboardButton(text=MAIN_MANUAL[lang])
            main_btns.add(btn7)
        await message.answer(text=SHARE_CONTACT_MESSAGE[lang], reply_markup=main_btns)
    else: await message.answer(text=NOT_OWN_NUMBER[lang])

@dp.message_handler()
async def reply_function(message: types.Message):
    clear_logs()
    telegram_id = message.from_user.id
    first_name = message.from_user.first_name
    r = requests.get(f"{BASIC_API}lang_get?telegram_id={telegram_id}")
    lang_data = r.json()
    lang = lang_data['data']

    r_phone_data = requests.get(f"{BASIC_API}get_phone?telegram_id={telegram_id}")
    phone_data = r_phone_data.json()
    phone = phone_data['data']['phone_number']

    # Hokim yordamchisi
    r_user_info = requests.get(f"{BASIC_API}get_user_info?phone={phone}")
    user_info = r_user_info.json()
    user_data = user_info['data']

    msg = message.text

    if msg in MAIN_APPEAL.values():
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, Appeals selected")
        apps = requests.get(f"{BASIC_API}get_appeals?phone={phone}")
        apps_data = apps.json()
        apps_data = apps_data['data']

        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
        if apps_data:
            apps_array_null = []
            for app_id in apps_data:
                ar_i = []
                i = app_id['id']
                text_app_id = f"{get_date(app_id['created_at'])}  {get_id(i)}  " \
                              f"{get_icon(app_id['doc_status'])}  {app_id['fullname']}"
                ar_i.append(text_app_id)
                ar_i.append(f"{PAGES}appeals_history?appeal_id={i}")
                apps_array_null.append(ar_i)

            btn_apps_null = (types.InlineKeyboardButton(text, url=url) for text, url in apps_array_null)
            web_btn = [
                types.InlineKeyboardButton(text=CREATE_APPEAL[lang], web_app=WebAppInfo(url=FORM_LINK_APP)),
                types.InlineKeyboardButton(text=CREATE_APPEAL_SHTAB[lang], web_app=WebAppInfo(url=FORM_LINK_SHTAB))
            ]

            for btn in btn_apps_null:
                keyboard_markup.add(btn)
            keyboard_markup.add(*web_btn)

            if len(user_data) != 0 and user_data['level'] == 4 and user_data['org_type'] == 100:
                btn_dist_app = types.InlineKeyboardButton(text=HOKIM_APPS[lang], callback_data='hokim_apps')
                keyboard_markup.add(btn_dist_app)

            await message.answer(text=APPEALS[lang], reply_markup=keyboard_markup)

        else:
            web_btn = [
                types.InlineKeyboardButton(text=CREATE_APPEAL[lang], web_app=WebAppInfo(url=FORM_LINK_APP)),
                types.InlineKeyboardButton(text=CREATE_APPEAL_SHTAB[lang], web_app=WebAppInfo(url=FORM_LINK_SHTAB))
            ]
            keyboard_markup.add(*web_btn)
            if len(user_data) != 0 and user_data['level'] == 4 and user_data['org_type'] == 100:
                btn_dist_app = types.InlineKeyboardButton(text=HOKIM_APPS[lang], callback_data='hokim_apps')
                keyboard_markup.add(btn_dist_app)
            await message.answer(text=EMPTY_APPS_LIST[lang], reply_markup=keyboard_markup)

    elif msg in MAIN_SUBSIDY.values():
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, Subsidy selected")
        r_subs = requests.get(f"{BASIC_API}get_subs?phone={phone}")
        subs_data = r_subs.json()
        subs_apps = subs_data['data']

        subsidy_markup = types.InlineKeyboardMarkup(row_width=1)
        if subs_apps:
            apps_array = []
            apps_array_null = []
            for app_id in subs_apps:
                ar_i = []
                i = app_id['id']
                text_app_id = f"{get_date(app_id['created_at'])}  {get_id(i)}  " \
                              f"{get_icon(app_id['doc_status'])} {app_id['sender_name']}"
                ar_i.append(text_app_id)
                if app_id['doc_short_url']:
                    ar_i.append(app_id['doc_short_url'])
                    apps_array.append(ar_i)
                else:
                    ar_i.append(f"url_not_found")
                    apps_array_null.append(ar_i)

            btn_apps = (types.InlineKeyboardButton(text, url=url) for text, url in apps_array)
            btn_apps_null = (types.InlineKeyboardButton(text, callback_data=data) for text, data in apps_array_null)
            web_subs_btn = types.InlineKeyboardButton(text=SUBS_APPL[lang], web_app=WebAppInfo(url=FORM_LINK_SUBS))

            subsidy_markup.add(*btn_apps)
            subsidy_markup.add(*btn_apps_null)
            subsidy_markup.add(web_subs_btn)

            if len(user_data) != 0 and user_data['level'] == 4 and user_data['org_type'] == 100:
                btn_dist_app = types.InlineKeyboardButton(text=HOKIM_SUBS[lang], callback_data='hokim_subs')
                subsidy_markup.add(btn_dist_app)

            await message.answer(text=SUBSIDIES[lang], reply_markup=subsidy_markup)
        else:
            web_subs_btn = types.InlineKeyboardButton(text=SUBS_APPL[lang], web_app=WebAppInfo(url=FORM_LINK_SUBS))
            if len(user_data) != 0 and user_data['level'] == 4 and user_data['org_type'] == 100:
                btn_dist_app = types.InlineKeyboardButton(text=HOKIM_SUBS[lang], callback_data='hokim_subs')
                subsidy_markup.add(btn_dist_app)
            subsidy_markup.add(web_subs_btn)
            await message.answer(text=NOT_FOUND_SUBSIDIES[lang], reply_markup=subsidy_markup)

    elif msg in MAIN_EMPLOYMENT.values():
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, Employment selected")
        url = f"{TABLE_EMP}recruited_people"
        if user_data:
            url = f"{TABLE_EMP}recruited_people?obl_id={user_data['obl_id']}&" \
                  f"area_id={user_data['area_id']}&district_id={user_data['district_id']}"
        employ_markup = types.InlineKeyboardMarkup(
            row_width=2,
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text=EMPLOY_INLINE[lang], web_app=WebAppInfo(url=FORM_LINK_EMPLOY)),
                    types.InlineKeyboardButton(text=EMPLOY_INLINE_YMMT[lang],
                                               web_app=WebAppInfo(url=FORM_LINK_YMMT))
                ],
                [types.InlineKeyboardButton(text='🌐  ' + GOTO_SITE_EMPLOY[lang], url=url)]
            ]
        )
        await message.answer(text=THESE_TEXT_EMP[lang], reply_markup=employ_markup)

    elif msg in MAIN_REFERRAL.values():
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, Referral selected")
        url = f"{PAGES}studying_people"
        if user_data:
            url = f"{PAGES}studying_people?obl_id={user_data['obl_id']}&" \
                  f"area_id={user_data['area_id']}&district_id={user_data['district_id']}"
        referral_markup = types.InlineKeyboardMarkup(
            row_width=2,
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(text=REF_INLINE_MONO[lang], web_app=WebAppInfo(url=FORM_LINK_MONO)),
                    types.InlineKeyboardButton(text=REF_INLINE_NNT[lang], web_app=WebAppInfo(url=FORM_LINK_NNT))
                ],
                [types.InlineKeyboardButton(text='🌐  ' + GOTO_SITE_REFER[lang], url=url)]
            ]
        )
        await message.answer(text=THESE_TEXT_REF[lang], reply_markup=referral_markup)

    elif msg in MAIN_BUSINESES.values():
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, Busineses selected")
        await message.answer(text=TEXT_BUS[lang])
        at_time = excel_bus("busines", "get_bus_survey", user_data['district_id'])
        await bot.send_document(chat_id=telegram_id, document=open(f'Тадбиркорлик субектлари{at_time}.xlsx', 'rb'))
        os.remove(f'Тадбиркорлик субектлари{at_time}.xlsx')

    elif msg in MAIN_NOTEBOOKS.values():
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, Notebooks selected")
        notes_markup = types.InlineKeyboardMarkup(
            row_width=2,
            inline_keyboard=[
                [types.InlineKeyboardButton(text=WOMEN[lang], callback_data='women'),
                 types.InlineKeyboardButton(text=YOUNG[lang], callback_data='young')],
                [types.InlineKeyboardButton(text=IRON[lang], callback_data='iron'),
                 types.InlineKeyboardButton(text=UNEMPLOYED[lang], callback_data='unemp')],
                [types.InlineKeyboardButton(text=SOCIAL_REGISTER[lang], callback_data='social')]
            ]
        )
        await message.answer(text=DOWN_NOTEBOOKS[lang], reply_markup=notes_markup)

    elif msg in MAIN_ACTS.values():
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, Notebooks selected")
        acts_markup = types.InlineKeyboardMarkup(
            row_width=1,
            inline_keyboard=[
                [types.InlineKeyboardButton(text=ADD_ACT[lang], url=FORM_LINK_ACT)],
                [types.InlineKeyboardButton(text=VIEW_ACTS[lang], url=f"{PAGES}family_business_info?report=1&"
                                                                      f"tab=survey_info&obl_id={user_data['obl_id']}&"
                                                                      f"area_id={user_data['area_id']}&"
                                                                      f"district_id={user_data['district_id']}")]
            ]
        )
        await message.answer(text=UNIT_ACTS[lang], reply_markup=acts_markup)

    elif msg in MAIN_MANUAL.values():
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, Manual selected")
        await bot.send_document(chat_id=telegram_id, document=DOC_URL)

    else:
        logging.info(msg=f"First_name: {first_name}, user_id: {telegram_id}, {time.asctime()}, message: {msg}")
        await message.answer(text=UNKNOWN_MESSAGE[lang])

class MahallaBot(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(MahallaBot, self).__init__(*args, **kwargs)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        executor.start_polling(dp, skip_updates=True)
