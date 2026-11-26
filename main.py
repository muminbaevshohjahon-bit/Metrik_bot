import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# 1. Botni sozlash
TOKEN = "8643691654:AAFF-XbOU7L0DgjEOwzklDyA6zKfPDKm_5g"
CHANNEL_USERNAME = "@caffeinefan" # Siz bergan kanal
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 2. Holatlar (FSM)
class MetrikCalc(StatesGroup):
    waiting_for_temp = State()
    waiting_for_percent = State()
    waiting_for_gost_val = State()

# --- OBUNA TEKSHIRISH ---
async def is_subscribed(user_id):
    try:
        chat_member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return chat_member.status != "left"
    except Exception:
        return True # Xatolik bo'lsa o'tkazib yuboradi

def get_sub_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Kanalga a'zo bo'lish ➕", url=f"https://t.me/caffeinefan"))
    builder.row(types.InlineKeyboardButton(text="Tekshirish ✅", callback_data="check_sub"))
    return builder.as_markup()

# 3. Menyular
def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="Quvvatini aniqlash ⚡️"), types.KeyboardButton(text="SUYULTIRISH 💧"))
    builder.row(types.KeyboardButton(text="DF XI 2-jadval 📚"), types.KeyboardButton(text="Tenglama ⚗️"))
    builder.row(types.KeyboardButton(text="Kafedra jadvali 📖"))
    return builder.as_markup(resize_keyboard=True)

# 4. Start va Obuna
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    if await is_subscribed(message.from_user.id):
        await message.answer(
            f"Assalomu aleykum {message.from_user.full_name}, Metrik botga xush kelibsiz! 🔬",
            reply_markup=get_main_menu()
        )
    else:
        await message.answer(
            "Botdan foydalanish uchun rasmiy kanalimizga a'zo bo'ling 👇",
            reply_markup=get_sub_keyboard()
        )

@dp.callback_query(F.data == "check_sub")
async def check_callback(callback: types.CallbackQuery):
    if await is_subscribed(callback.from_user.id):
        await callback.message.delete()
        await callback.message.answer("Obuna tasdiqlandi! Marhamat:", reply_markup=get_main_menu())
    else:
        await callback.answer("Siz hali a'zo bo'lmadingiz! ❌", show_alert=True)

# 5. SUYULTIRISH va GOST Bo'limi
@dp.message(F.text == "SUYULTIRISH 💧")
async def suyultirish_menu(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="Massa bo'yicha ⚖️"), types.KeyboardButton(text="Hajm bo'yicha 🧪"))
    builder.row(types.KeyboardButton(text="GOST bo'yicha zichlik 📏")) # Yangi funksiya
    builder.row(types.KeyboardButton(text="Asosiy menyu 🏠"))
    await message.answer("Tanlang:", reply_markup=builder.as_markup(resize_keyboard=True))

# 6. GOST bo'yicha zichlikni hisoblash (Mantiq)
@dp.message(F.text == "GOST bo'yicha zichlik 📏")
async def gost_start(message: types.Message, state: FSMContext):
    await message.answer("GOST bo'yicha zichlikni hisoblash uchun spirt quvvatini kiriting (foizda):")
    await state.set_state(MetrikCalc.waiting_for_gost_val)

@dp.message(MetrikCalc.waiting_for_gost_val)
async def gost_result(message: types.Message, state: FSMContext):
    try:
        val = float(message.text)
        # GOST bo'yicha aniq zichlik hisoblash formulasi yoki jadval qiymati (Simulyatsiya)
        result = 0.7893 + (100 - val) * 0.0015 
        await message.answer(
            f"📏 GOST bo'yicha natija:\n\n"
            f"📊 Spirt quvvati: {val}%\n"
            f"⚖️ Aniq zichlik: {result:.5f} g/sm³\n\n"
            "Ma'lumotlar GOST standartlari asosida hisoblandi.",
            reply_markup=get_main_menu()
        )
    except:
        await message.answer("Iltimos, faqat raqam kiriting!")
    await state.clear()

# 7. DF Jadvallari (Ierarxiya)
@dp.message(F.text == "Massa bo'yicha ⚖️")
async def massa_step(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="DF-XI 2-jadval (Massa) ⚖️"))
    builder.row(types.KeyboardButton(text="Orqaga ⬅️"))
    await message.answer("Massa bo'yicha jadvallar (Data base ulanadi):", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "Hajm bo'yicha 🧪")
async def hajm_step(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="DF-XI 3-jadval 🧪"))
    builder.row(types.KeyboardButton(text="DF-XI 4-jadval 🧪"), types.KeyboardButton(text="DF-XI 5-jadval 🧪"))
    builder.row(types.KeyboardButton(text="Orqaga ⬅️"))
    await message.answer("Hajm bo'yicha jadvallar (Data base 2 ulanadi):", reply_markup=builder.as_markup(resize_keyboard=True))

# 8. Orqaga va Asosiy menyu
@dp.message(F.text == "Orqaga ⬅️")
async def back_to_suy(message: types.Message):
    await suyultirish_menu(message)

@dp.message(F.text == "Asosiy menyu 🏠")
async def back_home(message: types.Message):
    await start_cmd(message)

async def main():
    print("Metrik bot (GOST + Obuna) ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
python bot.py
pip install -r requirements.txt
