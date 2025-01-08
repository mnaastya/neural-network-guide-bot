from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Ваш токен бота
TOKEN = "7426188484:AAEEicHGWrsmRgcUXSo8Jd6eR3AgOUD2mc8"

# Словарь с URL-адресами изображений для нейросетей (путь к изображениям на вашем ПК)
network_images = {
    "CHATGPT": "images/GPT.jpg",
    "BERT": "images/bert.jpg",
    "T5": "images/t5.jpg",
    "XLNet": "images/xlnet.jpg",
    "Stable Diffusion": "images/stable_diffusion.jpg",
    # Добавьте другие нейросети
}

# Словарь для быстрых гайдов
quick_guide_categories = {
    "text": {
        "title": "Текст",
        "networks": ["CHATGPT", "HUGGING FACE", "REPLICA"]
    },
    "image": {
        "title": "Изображения",
        "networks": ["FUSION BRAIN", "CRAIYON", "STABLE DIFFUSION", "ARTBREEDER"]
    },
    "video": {
        "title": "Видео",
        "networks": ["KLING", "RUNWAY ML", "DEEPFACELAB"]
    },
    "education": {
        "title": "Образование и обучение",
        "networks": ["QUIZLET", "KHAN ACADEMY + KHANMIGO", "SOCRATIC BY GOOGLE"]
    },
    "music": {
        "title": "Музыка",
        "networks": ["MAGENTA", "JUKEBOX"]
    }
    
}

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.delete()  # Удаление стартового сообщения
    keyboard = [[InlineKeyboardButton("Бесплатный быстрый гайд", callback_data="quick_guide")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Привет! ☺ Я помогу тебе быстро освоиться в мире нейросетей. Выбери обучение, которое хочешь пройти:",
        reply_markup=reply_markup
    )

# Функция обработки нажатия кнопки "Быстрый гайд"
async def handle_quick_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.delete()  # Удаление предыдущего сообщения
    await query.answer()

    # Генерация кнопок для категорий
    keyboard = [
        [InlineKeyboardButton(category["title"], callback_data=f"category_{key}")]
        for key, category in quick_guide_categories.items()
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "Для начала давай определимся, с какой категорией нейросетей ты хочешь ознакомиться? Выбери категорию:",
        reply_markup=reply_markup
    )

# Функция обработки выбора категории
async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.delete()  # Удаление предыдущего сообщения
    await query.answer()

    # Получение ключа категории
    category_key = query.data.replace("category_", "")
    category = quick_guide_categories.get(category_key)

    if not category:
        await query.message.reply_text("Такой категории нет.")
        return

    # Генерация кнопок для нейросетей
    keyboard = [
        [InlineKeyboardButton(network, callback_data=f"network_{network}")]
        for network in category["networks"]
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data="quick_guide")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        f"За категорию '{category['title']}' отвечает несколько нейросетей. Выбери ту, с которой хочешь начать:",
        reply_markup=reply_markup
    )

# Функция обработки выбора нейросети
async def handle_network_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.delete()  # Удаление предыдущего сообщения
    await query.answer()

    # Получение названия нейросети
    network_name = query.data.replace("network_", "")

    # Получение пути к изображению для выбранной нейросети
    image_path = network_images.get(network_name)

    if image_path:
        # Проверка, существует ли файл изображения, и отправка его
        try:
            with open(image_path, "rb") as photo:
                await query.message.reply_photo(photo=photo, caption=f"Вы выбрали нейросеть: {network_name}")
        except FileNotFoundError:
            await query.message.reply_text(f"Изображение для нейросети {network_name} не найдено.")
    else:
        # Если изображения нет
        await query.message.reply_text(f"Вы выбрали нейросеть: {network_name}")

# Функция обработки кнопки "Назад"
async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.delete()  # Удаление предыдущего сообщения
    await query.answer()

    keyboard = [[InlineKeyboardButton("Быстрый гайд", callback_data="quick_guide")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        "Привет! ☺ Я помогу тебе быстро освоиться в мире нейросетей. Выбери обучение, которое хочешь пройти:",
        reply_markup=reply_markup
    )

# Основной код
def main():
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()

    # Обработчики команд и кнопок
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_quick_guide, pattern="^quick_guide$"))
    app.add_handler(CallbackQueryHandler(handle_category_selection, pattern="^category_"))
    app.add_handler(CallbackQueryHandler(handle_network_selection, pattern="^network_"))
    app.add_handler(CallbackQueryHandler(handle_back, pattern="^back$"))

    # Запуск бота
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    app.run_polling()

if __name__ == "__main__":
    main()
