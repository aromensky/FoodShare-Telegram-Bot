from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Добро пожаловать в FoodShare!\nВведите /help для получения списка доступных команд.")

# Обработчик команды /help
def help(update, context):
    text = "/add_item - добавить продукт\n" \
           "/list_items - список добавленных продуктов\n" \
           "/find_item - найти продукт по названию\n" \
           "/delete_item - удалить продукт из списка\n" \
           "/cancel - отменить текущее действие"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

# Обработчик команды /list_items
def list_items(update, context):
    # Получаем список продуктов из хранилища данных
    items = context.user_data.get('items', [])
    
    # Если список продуктов пуст, сообщаем об этом пользователю
    if not items:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Список продуктов пуст.")
    else:
        # Формируем текст сообщения со списком продуктов
        text = "Список продуктов:\n\n"
        for i, item in enumerate(items):
            text += f"{i+1}. {item}\n"
        
        # Отправляем сообщение с списком продуктов пользователю
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

# Обработчик команды /find_item
def find_item(update, context):
    pass

# Обработчик команды /add_item
def add_item(update, context):
    pass

# Обработчик команды /delete_item
def delete_item(update, context):
    pass

# Обработчик команды /cancel
def cancel(update, context):
    # Удаляем все данные о текущем действии пользователя
    context.user_data.clear()
    
    # Отправляем сообщение с подтверждением отмены
    context.bot.send_message(chat_id=update.effective_chat.id, text="Действие отменено.", reply_markup=ReplyKeyboardRemove())

# Функция для обработки текстовых сообщений
def handle_text(update, context):
    # Получаем текст сообщения пользователя
    text = update.message.text
    
    # Получаем состояние конечного автомата пользователя
    state = context.user_data.get('state', 'START')
    
    if state == 'START':
        if text == '/add_item':
            # Переходим к добавлению продукта
            context.user_data['state'] = 'ADD_ITEM'
            context.bot.send_message(chat_id=update.effective_chat.id, text="Введите название продукта:", reply_markup=ReplyKeyboardRemove())
        elif text == '/list_items':
            
            # Переходим к просмотру списка продуктов
            list_items(update, context)
        elif text == '/find_item':
            
            # Переходим к поиску прод
            bot.send_message(chat_id=chat_id, text='Введите название продукта, который вы ищете:')
       
            # переключаем состояние пользователя на поиск товара
            user_states[user_id] = SEARCH_ITEM_STATE
        
    # Обработчик команды /add_item
    elif text == '/add_item':
        bot.send_message(chat_id=chat_id, text='Введите название продукта, который вы хотите отдать:')
        
        # переключаем состояние пользователя на добавление товара
        user_states[user_id] = ADD_ITEM_STATE

    # Обработчик текстовых сообщений в состоянии SEARCH_ITEM_STATE
    elif user_states[user_id] == SEARCH_ITEM_STATE:
        # Получаем список товаров, которые пользователи отдают
        items = db.search_items(text)
        
        # Если товары найдены, выводим список
        if items:
            message = 'Найденные товары:\n'
            for item in items:
                message += f'- {item[0]} ({item[1]}шт.)\n'
        else:
            message = 'Извините, но товары по вашему запросу не найдены.'
        
        # Выводим сообщение пользователю
        bot.send_message(chat_id=chat_id, text=message)
        
        # переключаем состояние пользователя на исходное
        user_states[user_id] = DEFAULT_STATE

    # Обработчик текстовых сообщений в состоянии ADD_ITEM_STATE
    elif user_states[user_id] == ADD_ITEM_STATE:
        # Записываем товар в базу данных
        db.add_item(user_id, text)
        
        # Выводим сообщение пользователю
        bot.send_message(chat_id=chat_id, text='Спасибо, ваш товар был добавлен в список!')
        
        # переключаем состояние пользователя на исходное
        user_states[user_id] = DEFAULT_STATE
    
    # Обработчик команды /list_items
    elif text == '/list_items':
        # Получаем список товаров пользователя из базы данных
        items = db.get_items(user_id)
        
        # Формируем сообщение со списком товаров
        message = 'Ваши товары:\n\n'
            for i, item in enumerate(items):
                message += f'{i+1}. {item}\n'
        
        # Если список товаров пуст, сообщаем об этом
        if not items:
        message = 'У вас пока нет товаров в списке'
        
        # Выводим сообщение пользователю
        bot.send_message(chat_id=chat_id, text=message)
    
    # Обработчик команды /find_item
    elif text == '/find_item':
        
        # Устанавливаем состояние пользователя в поиске товара
        user_states[user_id] = FIND_ITEM_STATE
        
        # Выводим сообщение с запросом описания товара
        bot.send_message(chat_id=chat_id, text='Введите описание товара, который вы ищете')
    
    # Обработчик текстовых сообщений в состоянии FIND_ITEM_STATE
    elif user_states[user_id] == FIND_ITEM_STATE:
        
        # Получаем список товаров пользователя из базы данных
        items = db.get_items(user_id)
        
        # Ищем товары, которые содержат введенное пользователем описание
        found_items = []
            for item in items:
                if text.lower() in item.lower():
                    found_items.append(item)

        # Формируем сообщение с найденными товарами
        message = f'Найдено {len(found_items)} товаров:\n\n'
            for i, item in enumerate(found_items):
                message += f'{i+1}. {item}\n'

            # Если ничего не найдено, сообщаем об этом
                if not found_items:
                message = 'Ничего не найдено'

        # Выводим сообщение пользователю
        bot.send_message(chat_id=chat_id, text=message)
        
     # Обработчик неизвестной команды
     else:
        bot.send_message(chat_id=chat_id, text='Неизвестная команда. Введите /help, чтобы узнать доступные команды')
        
