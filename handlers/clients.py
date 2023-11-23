from create_bot import dp,bot
from aiogram.dispatcher import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from parse import product_links

intro_message = (
    "Привет! 🌟\n"
    "Добро пожаловать в магазин Xiaomi Redmi в Бишкеке! 📱\n"
    "Твой помощник в мире техники. Рассрочка через бота! 💳🤖\n\n"
    "📢 Информация о товарах и акциях\n"
    "🛒 Оформление заказов\n"
    "❓ Ответы на вопросы\n"
    "🚀 Помощь в выборе гаджетов\n\n"
    "Сделай покупки веселыми и удобными с нами! 😊👍"
)



# Create a dictionary to store message IDs
previous_messages = {}
cart = {}

# @dp.message_handler(commands=["start"])
async def start(message: types.Message, state: FSMContext):
    button1 = InlineKeyboardButton("Phones", callback_data="phones")
    button2 = InlineKeyboardButton("TV", callback_data="option2")
    button3 = InlineKeyboardButton("Loptop", callback_data="option3")
    button4 = InlineKeyboardButton("House electronic", callback_data="option4")
    button5 = InlineKeyboardButton("Watch", callback_data="option5")
    button6 = InlineKeyboardButton("Wireless", callback_data="option6")
    button7 = InlineKeyboardButton("Med Electronic", callback_data="option7")
    button8 = InlineKeyboardButton("Scooter", callback_data="option8")
    button9 = InlineKeyboardButton("/start", callback_data="start")
    button10 = InlineKeyboardButton("/Корзина", callback_data="Корзина")

    # Create four rows with consistent button size
    row1 = [button1, button2, button3, button4]
    row2 = [button5, button6, button7, button8]
    row3 = [button9,button10]

    # Create the keyboard with rows
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*row1)
    keyboard.add(*row2)
    keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard1.add(*row3)

    # Send a message with the inline keyboard and the intro_message
    await message.answer(intro_message, reply_markup=keyboard)
    await message.answer("Чтобы выйти на меню Нажмите на START\nЧтобы посмотреть корзину Нажмите на Корзина",reply_markup=keyboard1)


@dp.message_handler(commands=["adres"])
async def adress(message:types.Message):
    await message.answer(text="Наш Адресс ")
# Define a callback handler for the "Phones" button
# @dp.callback_query_handler(lambda query: query.data == "phones")
async def get_phones(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    await state.finish()
    await state.update_data(link_index=0)  # Start with the first link
    await show_link(callback_query.message, state)


async def filtered(message: types.Message):
    user_input = message.text.lower()  # Convert user input to lowercase for easier comparison

    if "filter" in user_input:
        # Handle filtering logic based on user input
        await message.answer("Filtering products...")

    elif "info" in user_input:
        # Provide information based on user input
        await message.answer("Here's some information about our products...")

    else:
        # Handle unrecognized commands or messages
        await message.answer("I'm not sure what you want. Please use valid commands.")




async def paginate_links(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    link_index = data.get("link_index")

    if link_index is None:
        link_index = 0

    if callback_query.data == "next" and link_index < len(product_links) - 1:
        link_index += 1
    elif callback_query.data == "prev" and link_index > 0:
        link_index -= 1

    await state.update_data(link_index=link_index)
    await delete_previous_message(callback_query.message)
    await show_link(callback_query.message, state)
    return await callback_query.answer()


async def show_link(message: types.Message, state: FSMContext):
    data = await state.get_data()
    link_index = data.get("link_index")

    if link_index is None:
        link_index = 0

    link = product_links[link_index]
    button6 = InlineKeyboardButton("Предыдуший", callback_data = "prev")
    button7 = InlineKeyboardButton("Следуший", callback_data="next")
    button8 = InlineKeyboardButton("Дбавить товар", callback_data="add_to_cart")

    # Create four rows with consistent button size
    row2 = [button6, button7, button8]
    # Create the keyboard with rows
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*row2)


    # Send the new message and store its message ID
    new_message = await message.answer(link, reply_markup=keyboard)
    previous_messages[message.chat.id] = new_message.message_id


cart = []


# ...

async def add_to_cart(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    link_index = data.get("link_index")
    link = product_links[link_index]

    # Check if the product is already in the cart
    product_in_cart = next((item for item in cart if item[0] == link), None)

    if product_in_cart is None:
        # If the product is not in the cart, add it as a tuple (link, quantity)
        cart.append((link, 1))
    else:
        # If the product is already in the cart, increase its quantity
        index = cart.index(product_in_cart)
        cart[index] = (link, product_in_cart[1] + 1)

    await callback_query.answer("Товар добавлен в корзину!")


# @dp.message_handler(Command("cart"))
# Define cart as a list of tuples where each tuple contains (product link, quantity)

# ...
async def buy_product(callback_query: types.CallbackQuery, state: FSMContext):
    if not cart:
        await callback_query.answer("Корзина пуста.")
    else:
        total_price = 0  # Initialize the total price to calculate the final cost
        cart_items_text = []  # Create a list to store cart items as text

        for link, quantity in cart:
            # Calculate the total price for each item and update the total price
            # You need to add your logic to fetch the actual price for the product based on 'link'
            # For now, let's assume a static price of 100 for each product
            product_price = 100  # Replace with your logic to get the actual price
            item_price = product_price * quantity
            total_price += item_price

            # Create a text representation of the cart item
            cart_item_text = f"Товар: {link}\nКоличество: {quantity}\nЦена за товар: {product_price}\nОбщая цена: {item_price}\n"
            cart_items_text.append(cart_item_text)

        # Combine all cart items into a single text
        cart_text = "\n".join(cart_items_text)

        # Provide the total price and offer payment options
        cart_text += f"\nИтоговая стоимость: {total_price}\n"
        cart_text += "Выберите способ оплаты:\n"

        # Add buttons for payment options
        button1 = InlineKeyboardButton("Оплата онлайн", callback_data="cash_payment")
        button2 = InlineKeyboardButton("Рассрочка", callback_data="online_payment")

        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(button1, button2)

        await bot.send_message(callback_query.message.chat.id, cart_text, reply_markup=keyboard)


async def view_cart(message: types.Message):
    button1 = InlineKeyboardButton("Купить Товар", callback_data="BUY")
    keyboard = InlineKeyboardMarkup()
    row = [button1]
    keyboard.add(*row)
    if not cart:
        await message.answer("Корзина пуста.")
    else:
        cart_items = [f"{link}: {quantity}" for link, quantity in cart]
        cart_text = "\n".join(cart_items)
        await message.answer(f"Содержимое корзины:\n{cart_text}", reply_markup=keyboard)


async def delete_previous_message(message: types.Message):
    chat_id = message.chat.id
    if chat_id in previous_messages:
        previous_message_id = previous_messages[chat_id]
        try:
            await bot.delete_message(chat_id, previous_message_id)
        except Exception as e:
            print(f"Failed to delete message: {e}")


def register_handlers_clients(dp:Dispatcher):
    dp.register_message_handler(start,commands=["start"])
    dp.register_message_handler(filtered, commands=["filtered"])
    dp.register_callback_query_handler(buy_product, lambda callback_query: callback_query.data == "BUY")
    # dp.register_callback_query_handler(start, lambda query: query.data == "start")
    # dp.register_callback_query_handler(view_cart, lambda query: query.data == "Корзина")
    dp.register_callback_query_handler(get_phones,lambda query: query.data == "phones")
    dp.register_callback_query_handler(paginate_links,lambda callback_query: callback_query.data in ["next", "prev"])
    dp.register_callback_query_handler(add_to_cart,lambda callback_query: callback_query.data == "add_to_cart")
    dp.register_message_handler(view_cart,commands=["Корзина"])
