import sqlite3
import random
import logging
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token="TOKEN")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
taraflar = ["⬅️ Chapga", "⬆️ O'rtaga", "➡️ O'ngga"]

class Form(StatesGroup):
	UserTepish = State()
	ComputerTepish = State()
	tepdi = State()

def main_menu():
	markup = types.ReplyKeyboardRemove()
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
	btn1 = types.KeyboardButton("⚽️ O'yinni boshlash" )
	btn2 = types.KeyboardButton("📊 O'yinga baho berish")

	markup.add(btn1, btn2)
	return markup

def ui_menu():
	markup = types.ReplyKeyboardRemove()
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
	btn1 = types.KeyboardButton("⬅️ Chapga" )
	btn2 = types.KeyboardButton("⬆️ O'rtaga")
	btn3 = types.KeyboardButton("➡️ O'ngga")
	btn4 = types.KeyboardButton("🛑 O'yinni yakunlash")

	markup.add(btn1, btn2, btn3, btn4)
	return markup	


def add_db(m):
	conn = sqlite3.connect("mydata7.db") # или :memory: чтобы сохранить в RAM
	cursor = conn.cursor()
	#try:
	cursor.execute('CREATE TABLE IF NOT EXISTS user2 (id INTEGER UNIQUE)')
	#except:
	#	pass		

	try:
		cursor.execute("""INSERT INTO user2
				  VALUES (?)""", (m,)
			   )
		conn.commit()
	except:
		pass

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	add_db(message.chat.id)
	await bot.send_message(message.chat.id, "Assalomu alaykum, penalti bo'tga xush kelibsiz.\nO'yinni boshlash uchun quyidagi tugmani bosing👇", parse_mode='html', reply_markup=main_menu())
	
	try:
		await bot.send_message(-1001199004814, f"{message.from_user.first_name} - {message.chat.id} Futbol botdan foydalanishni boshladi")
	except:
		pass

@dp.message_handler(commands=['users'])
async def send_welcome(message: types.Message):
	try:
		conn = sqlite3.connect("mydata7.db") # или :memory: чтобы сохранить в RAM
		cursor = conn.cursor()
		try:
			cursor.execute('CREATE TABLE user2 (id INTEGER UNIQUE)')
		except:
			pass

		cursor.execute("SELECT id FROM user2")
		Lusers = cursor.fetchall()
		users=[]
		count=len(Lusers)
		await bot.send_message(message.chat.id, f"👥Total number of users: {count}")


	except:
		pass

@dp.message_handler(commands=['send_database'])
async def send_db(message: types.Message):
	document = open('mydata7.db', 'rb')
	await bot.send_document(message.chat.id, document)	

@dp.message_handler(state=None)
async def echo_message(message: types.Message, state: FSMContext):
	if message.text == "⚽️ O'yinni boshlash":
		await bot.copy_message(message.chat.id,-1001636110165,  2)
		await bot.send_message(message.chat.id, "Qaysi tarafga tepasiz?", reply_markup=ui_menu())
		
		async with state.proxy() as data:
			data["user"] = 0
			data["computer"] = 0
			data["user_shoots"] = ""
			data["comp_shoots"] = ""
			data["comp_zarbalari"] = 0
			data["tepdi"] = False
			data["comp_tepdi"] = False

		await Form.UserTepish.set()
	elif message.text == "📊 O'yinga baho berish":
		await bot.forward_message(message.chat.id,-1001636110165,  26)
		await bot.send_message(message.chat.id, "Biz bilan bog'lanish uchun @young_progers kanaliga o'ting.")
	else:
		await bot.send_message(message.chat.id, "Kerakli tugmani bosing👇")

@dp.message_handler(state=Form.UserTepish)
async def user_zarba(message: types.Message, state: FSMContext):
	comp_choice = random.choice(taraflar)

	if message.text == "🛑 O'yinni yakunlash": ###################
		await state.finish()
		await bot.send_message(message.chat.id, "O'yin yakunlandi", reply_markup=main_menu())

	elif message.text in taraflar:
		async with state.proxy() as data:
			#data["tepdi"] = True
			if data["tepdi"]:
				return
		if message.text == comp_choice:
			if comp_choice=="⬅️ Chapga":
				await bot.copy_message(message.chat.id,-1001636110165,  13)
			elif comp_choice=="⬆️ O'rtaga":
				await bot.copy_message(message.chat.id,-1001636110165,  15)			
			elif comp_choice=="➡️ O'ngga":
				await bot.copy_message(message.chat.id,-1001636110165,  14)

			async with state.proxy() as data:
				data["user_shoots"] += "🔴"
				data["tepdi"] = True
				

		elif message.text!=comp_choice:

			if comp_choice=="⬅️ Chapga" and message.text=="⬆️ O'rtaga":
				await bot.copy_message(message.chat.id,-1001636110165,  18)#
			elif comp_choice=="⬅️ Chapga" and message.text=="➡️ O'ngga":
				await bot.copy_message(message.chat.id,-1001636110165,  21)#
			elif comp_choice=="⬆️ O'rtaga" and message.text=="⬅️ Chapga":
				await bot.copy_message(message.chat.id,-1001636110165,  16)#
			elif comp_choice=="⬆️ O'rtaga" and message.text=="➡️ O'ngga":
				await bot.copy_message(message.chat.id,-1001636110165,  20)#
			elif comp_choice=="➡️ O'ngga" and message.text=="⬆️ O'rtaga":
				await bot.copy_message(message.chat.id,-1001636110165,  19)#
			else:
				await bot.copy_message(message.chat.id,-1001636110165,  17)#

			async with state.proxy() as data:
				data["user_shoots"] += "🟢"
				data["user"] += 1
				data["tepdi"] = True

		async with state.proxy() as data:
			data["comp_tepdi"]=False

		await asyncio.sleep(6)
		if message.text!=comp_choice:
			await bot.copy_message(message.chat.id,-1001636110165,  22)
		else:
			await bot.copy_message(message.chat.id,-1001636110165,  23)
		await bot.send_message(message.chat.id, f'👤 Siz: {data["user"]} {data["user_shoots"]}\n🤖Bot: {data["computer"]} {data["comp_shoots"]}')
		await asyncio.sleep(1)
		await bot.copy_message(message.chat.id,-1001636110165,  3)
		await bot.send_message(message.chat.id, "Qaysi tarafga otilasiz? ")

		await Form.ComputerTepish.set()

	else:
		await bot.send_message(message.chat.id, "Notog'ri tugmani bosdingiz, iltimos to'g'ri tugmani bosing👇")
		await Form.UserTepish.set()


@dp.message_handler(state=Form.ComputerTepish)
async def comp_zarba(message: types.Message, state: FSMContext):
	comp_choice = random.choice(taraflar)

	async with state.proxy() as data:
		data["comp_zarbalari"] += 1


	if message.text == "🛑 O'yinni yakunlash":
		await state.finish()
		await bot.send_message(message.chat.id, "O'yin yakunlandi", reply_markup=main_menu())


	elif message.text in taraflar:
		async with state.proxy() as data:	
			if data["comp_tepdi"]:
				return
			
		if message.text == comp_choice:
			
			if comp_choice=="⬅️ Chapga":
				await bot.copy_message(message.chat.id,-1001636110165,  4)
			elif comp_choice=="⬆️ O'rtaga":
				await bot.copy_message(message.chat.id,-1001636110165,  6)			
			elif comp_choice=="➡️ O'ngga":
				await bot.copy_message(message.chat.id,-1001636110165,  5)

			async with state.proxy() as data:
				data["comp_shoots"] += "🔴"
				data["comp_tepdi"] = True
				
		else:
			#["⬅️ Chapga", "⬆️ O'rtaga", "➡️ O'ngga"]

			if comp_choice=="⬅️ Chapga" and message.text=="⬆️ O'rtaga":
				await bot.copy_message(message.chat.id,-1001636110165,  7)
			elif comp_choice=="⬅️ Chapga" and message.text=="➡️ O'ngga":
				await bot.copy_message(message.chat.id,-1001636110165,  8)
			elif comp_choice=="⬆️ O'rtaga" and message.text=="⬅️ Chapga":
				await bot.copy_message(message.chat.id,-1001636110165,  9)
			elif comp_choice=="⬆️ O'rtaga" and message.text=="➡️ O'ngga":
				await bot.copy_message(message.chat.id,-1001636110165,  10)
			elif comp_choice=="➡️ O'ngga" and message.text=="⬆️ O'rtaga":
				await bot.copy_message(message.chat.id,-1001636110165,  11)
			else:
				await bot.copy_message(message.chat.id,-1001636110165,  12)



			async with state.proxy() as data:
				data["comp_shoots"] += "🟢"
				data["computer"] += 1
				data["comp_tepdi"] = True		
								
		
		await asyncio.sleep(6)
		if message.text!=comp_choice:
			await bot.copy_message(message.chat.id,-1001636110165,  22)
		else:
			await bot.copy_message(message.chat.id,-1001636110165,  23)


		async with state.proxy() as data:
			await bot.send_message(message.chat.id, f'👤 Siz: {data["user"]} {data["user_shoots"]}\n🤖Bot: {data["computer"]} {data["comp_shoots"]}')
			if data["comp_zarbalari"]<5 or data["user"]==data["computer"]:
				await asyncio.sleep(1)
				await bot.copy_message(message.chat.id,-1001636110165,  2)
				await bot.send_message(message.chat.id, "Qaysi tarafga tepasiz? ")			
				data["tepdi"]=False
				await Form.UserTepish.set()
			else:
				await state.finish()
				if data["user"]>data["computer"]:
					await bot.copy_message(message.chat.id,-1001636110165,  24)
					await bot.send_message(message.chat.id, "Kerakli tugmani bosing👇", reply_markup=main_menu())
				elif data["user"]<data["computer"]:
					await bot.copy_message(message.chat.id,-1001636110165,  25)
					await bot.send_message(message.chat.id, "Kerakli tugmani bosing👇", reply_markup=main_menu())
				
	else:
		await bot.send_message(message.chat.id, "Notog'ri tugmani bosdingiz, iltimos to'g'ri tugmani bosing👇")
		await Form.ComputerTepish.set()

if __name__ == '__main__':
	executor.start_polling(dp)
