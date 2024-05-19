from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
import mysql.connector
import asyncio
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# telegram 연결 설정 
TELEGRAM_BOT_TOKEN = '6417926677:AAFpFVg4zGjjytISsI7h5qsg6QHIEophjqc'
TELEGRAM_CHAT_ID = '7090041263'
# bot = Bot(token=TELEGRAM_BOT_TOKEN)

# MySQL 연결 설정
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0916",
    database="hotdeal"
)

# Constants for conversation states
KEYWORD_STATE = 1

# Function to fetch latest hot deals
def get_latest_hotdeals(cursor, limit=10):
    cursor.execute("SELECT * FROM deals ORDER BY date DESC LIMIT %s", (limit,))
    return cursor.fetchall()

# Function to fetch hot deals by keyword
def get_hotdeals_by_keyword(cursor, keyword):
    cursor.execute("SELECT * FROM deals WHERE title LIKE %s", (f"%{keyword}%",))
    return cursor.fetchall()

# Keyword input handler
async def keyword_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyword = update.message.text

    # Fetch hot deals by keyword
    cursor = connection.cursor(dictionary=True)
    hotdeals = get_hotdeals_by_keyword(cursor, keyword)
    cursor.close()

    # Send search results as message
    hotdeal_messages = [f"{deal['title']} (등록일:{deal['date']})\n\t→ {deal['deal_url']}" for deal in hotdeals]
    message_text = "\n".join(hotdeal_messages) if hotdeal_messages else "해당 키워드로 핫딜을 찾을 수 없습니다."
    await update.message.reply_text(message_text)

    # End conversation
    return ConversationHandler.END

# 최신 핫딜 버튼 핸들러
# async def latest_hotdeal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     cursor = connection.cursor(dictionary=True)
#     hotdeals = get_latest_hotdeals(cursor)
#     cursor.close()
#     for hotdeal in hotdeals:
#         message = f"{hotdeal['title']}"
#         update.message.reply_text(message)

# 키워드 핫딜 버튼 핸들러
# def keyword_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     message = "핫딜 키워드를 입력하세요."
#     update.message.reply_text(message)

# 키워드 입력 핸들러
# def keyword_input_handler(update, context):
#     keyword = update.message.text
#     cursor = connection.cursor(dictionary=True)
#     hotdeals = get_hotdeals_by_keyword(cursor, keyword)
#     cursor.close()
#     for deal in hotdeals:
#         message = f"{deal['title']}"
#         update.message.reply_text(message)


# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("최신 핫딜", callback_data='latest_hotdeal')],
        [InlineKeyboardButton("키워드 검색", callback_data='keyword')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("핫딜공유방 입장을 환영합니다.\n버튼을 선택해 주세요.", reply_markup=reply_markup)


# Callback handler for buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'latest_hotdeal':
        cursor = connection.cursor(dictionary=True)
        hotdeals = get_latest_hotdeals(cursor)
        cursor.close()

        hotdeal_messages = [f"{hotdeal['title']} (등록일:{hotdeal['date']})\n\t→ {hotdeal['deal_url']}" for hotdeal in hotdeals]
        message_text = "\n".join(hotdeal_messages) if hotdeal_messages else "최신 핫딜을 찾을 수 없습니다."
        await query.edit_message_text(text=message_text)

    elif query.data == 'keyword':
        await query.message.reply_text("검색하려는 키워드를 입력해주세요.")
        context.user_data['awaiting_keyword'] = True

# Handler to process keyword input
async def process_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_keyword'):
        keyword = update.message.text
        cursor = connection.cursor(dictionary=True)
        hotdeals = get_hotdeals_by_keyword(cursor, keyword)
        cursor.close()

        hotdeal_messages = [f"{deal['title']} (등록일:{deal['date']})\n\t→ {deal['deal_url']}" for deal in hotdeals]
        message_text = "\n".join(hotdeal_messages) if hotdeal_messages else "해당 키워드로 핫딜을 찾을 수 없습니다."
        await update.message.reply_text(message_text)

        # Reset keyword awaiting state
        context.user_data['awaiting_keyword'] = False
        
# Main function
if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlers
    start_handler = CommandHandler('start', start)
    button_handler = CallbackQueryHandler(button_handler)
    keyword_input_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, process_keyword)

    # Add handlers to application
    application.add_handler(start_handler)
    application.add_handler(button_handler)
    application.add_handler(keyword_input_handler)

    # Run bot
    application.run_polling()

# 버튼 메뉴 만들기
# def create_menu():
#     keyboard = [
#         [InlineKeyboardButton("최신 핫딜", callback_data='latest_hotdeal')],
#         [InlineKeyboardButton("키워드 검색", callback_data='keyword')]
#     ]
#     return InlineKeyboardMarkup(keyboard)

# 메시지에 버튼 메뉴 추가하기
# def send_menu(update, context):
#     menu = create_menu()
#     update.message.reply_text("원하는 항목을 선택하세요.", reply_markup=menu)

# 콜백 핸들러 설정
# application.add_handler(CommandHandler("start", send_menu))
# application.add_handler(CallbackQueryHandler(latest_hotdeal_handler, pattern='latest_hotdeal'))
# application.add_handler(CallbackQueryHandler(keyword_handler, pattern='keyword'))
# application.add_handler(MessageHandler(filters.text & ~filters.command, keyword_input_handler))

# Telegram 봇 시작
# application.run_polling()
# updater.start_polling()
# updater.idle()

# MySQL 연결 종료
# connection.close()



# async def send_hotdeal(connection):
#     cursor = connection.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM deals")
#     deals = cursor.fetchall()
#     cursor.close()

#     for deal in deals:
#         message = f'''{deal['title']}'''
#         await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# if __name__ == "__main__":
#     # MySQL 연결 설정
#     connection = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="0916",
#         database="hotdeal"
#     )

#     # 데이터베이스에서 정보 가져와서 메시지 보내기
#     asyncio.run(send_hotdeal(connection))

#     # MySQL 연결 종료
#     connection.close()