from aiogram import types



menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    types.KeyboardButton('👑 admin')
)

adm = types.ReplyKeyboardMarkup(resize_keyboard=True)
adm.add(
    types.KeyboardButton('👿 black list'),
    types.KeyboardButton('✅ add to blacklist'),
    types.KeyboardButton('❎ remove from black list')
)
adm.add(types.KeyboardButton('💬 Newsletter'))
adm.add('⏪ Back')

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back.add(
    types.KeyboardButton('⏪ Cancel')
)


def fun(user_id):
    quest = types.InlineKeyboardMarkup(row_width=3)
    quest.add(
        types.InlineKeyboardButton(text='💬 Reply', callback_data=f'{user_id}-ans'),
        types.InlineKeyboardButton(text='❎ Delete', callback_data='ignor')
    )
    return quest
