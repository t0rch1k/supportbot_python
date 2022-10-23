import logging
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, admin
import keyboard as kb
import functions as func
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import Throttled

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
connection = sqlite3.connect('data.db')
q = connection.cursor()

class st(StatesGroup):
	item = State()
	item2 = State()
	item3 = State()
	item4 = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('Welcome.', reply_markup=kb.menu)
		else:
			await message.answer('Hello, this is a support bot.\nWrite me your question and I will send it to the administration.\nFor spam / flood - blacklisted!')
	else:
		await message.answer('You got banned')


@dp.message_handler(content_types=['text'], text='👑 admin')
async def handfler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('Welcome to the admin panel.', reply_markup=kb.adm)

@dp.message_handler(content_types=['text'], text='⏪ Back')
async def handledr(message: types.Message, state: FSMContext):
	await message.answer('Welcome.', reply_markup=kb.menu)

@dp.message_handler(content_types=['text'], text='👿 blacklist')
async def handlaer(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			q.execute(f"SELECT * FROM users WHERE block == 1")
			result = q.fetchall()
			sl = []
			for index in result:
				i = index[0]
				sl.append(i)

			ids = '\n'.join(map(str, sl))
			await message.answer(f'ID of users in the blacklist:\n{ids}')

@dp.message_handler(content_types=['text'], text='✅ Add to blacklist')
async def hanadler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('Enter the ID of the user you want to block.\nClick the button below to cancel', reply_markup=kb.back)
			await st.item3.set()

@dp.message_handler(content_types=['text'], text='❎ Remove from blacklist')
async def hfandler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('Enter the ID of the user you want to unblock.\nClick the button below to cancel', reply_markup=kb.back)
			await st.item4.set()

@dp.message_handler(content_types=['text'], text='💬 Newsletter')
async def hangdler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			await message.answer('Enter text for newsletter.\n\nClick the button below to cancel', reply_markup=kb.back)
			await st.item.set()

@dp.message_handler(content_types=['text'])
@dp.throttled(func.antiflood, rate=3)
async def h(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id == admin:
			pass
		else:
			await message.answer('Message sent.')
			await bot.send_message(admin, f"<b>Got a new question!</b>\n<b>from:</b> {message.from_user.mention}\nID: {message.chat.id}\n<b>Message:</b> {message.text}", reply_markup=kb.fun(message.chat.id), parse_mode='HTML')
	else:
		await message.answer('You received a ban from the administration.')


@dp.callback_query_handler(lambda call: True)
async def cal(call, state: FSMContext):
	if 'ans' in call.data:
		a = call.data.index('-ans')
		ids = call.data[:a]
		await call.message.answer('Enter your answer:', reply_markup=kb.back)
		await st.item2.set()
		await state.update_data(uid=ids)
	elif 'ignor' in call.data:
		await call.answer('Removed')
		await bot.delete_message(call.message.chat.id, call.message.message_id)
		await state.finish()

@dp.message_handler(state=st.item2)
async def proc(message: types.Message, state: FSMContext):
	if message.text == '⏪ Cancel':
		await message.answer('Cancel! I return back.', reply_markup=kb.menu)
		await state.finish()
	else:
		await message.answer('Message sent.', reply_markup=kb.menu)
		data = await state.get_data()
		id = data.get("uid")
		await state.finish()
		await bot.send_message(id, 'You received a response from the administrator:\n\nText: {}'.format(message.text))

@dp.message_handler(state=st.item)
async def process_name(message: types.Message, state: FSMContext):
	q.execute(f'SELECT user_id FROM users')
	row = q.fetchall()
	connection.commit()
	text = message.text
	if message.text == '⏪ Cancel':
		await message.answer('Cancel! I return back.', reply_markup=kb.adm)
		await state.finish()
	else:
		info = row
		await message.answer('Newsletter started!', reply_markup=kb.adm)
		for i in range(len(info)):
			try:
				await bot.send_message(info[i][0], str(text))
			except:
				pass
		await message.answer('Newsletter completed!', reply_markup=kb.adm)
		await state.finish()


@dp.message_handler(state=st.item3)
async def proce(message: types.Message, state: FSMContext):
	if message.text == '⏪ Cancel':
		await message.answer('Cancel! I return back.', reply_markup=kb.adm)
		await state.finish()
	else:
		if message.text.isdigit():
			q.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
			result = q.fetchall()
			connection.commit()
			if len(result) == 0:
				await message.answer('This user was not found in the database.', reply_markup=kb.adm)
				await state.finish()
			else:
				a = result[0]
				id = a[0]
				if id == 0:
					q.execute(f"UPDATE users SET block = 1 WHERE user_id = {message.text}")
					connection.commit()
					await message.answer('The user has been successfully banned.', reply_markup=kb.adm)
					await state.finish()
					await bot.send_message(message.text, 'You received a ban from the administration.')
				else:
					await message.answer('This user has already been banned', reply_markup=kb.adm)
					await state.finish()
		else:
			await message.answer('You enter letters...\nEnter ID')

@dp.message_handler(state=st.item4)
async def proc(message: types.Message, state: FSMContext):
	if message.text == '⏪ Cancel':
		await message.answer('Cancel! I return back.', reply_markup=kb.adm)
		await state.finish()
	else:
		if message.text.isdigit():
			q.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
			result = q.fetchall()
			connection.commit()
			if len(result) == 0:
				await message.answer('This user was not found in the database.', reply_markup=kb.adm)
				await state.finish()
			else:
				a = result[0]
				id = a[0]
				if id == 1:
					q.execute(f"UPDATE users SET block = 0 WHERE user_id = {message.text}")
					connection.commit()
					await message.answer('The user has been successfully unbanned.', reply_markup=kb.adm)
					await state.finish()
					await bot.send_message(message.text, 'You have been unblocked by the administration.')
				else:
					await message.answer('This user has not been banned.', reply_markup=kb.adm)
					await state.finish()
		else:
			await message.answer('You enter letters...\nEnter ID')

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
