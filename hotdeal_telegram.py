from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
import mysql.connector
import asyncio
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

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

# 최신 핫딜 가져오기
def get_latest_hotdeals(cursor, limit=20):
    cursor.execute("SELECT * FROM deals ORDER BY date DESC LIMIT %s", (limit,))
    return cursor.fetchall()

# 키워드로 핫딜 가져오기
def get_hotdeals_by_keyword(cursor, keyword):
    cursor.execute("SELECT * FROM deals WHERE title LIKE %s", (f"%{keyword}%",))
    return cursor.fetchall()

# 최신 핫딜 버튼 핸들러
async def latest_hotdeal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor = connection.cursor(dictionary=True)
    hotdeals = get_latest_hotdeals(cursor)
    cursor.close()
    for hotdeal in hotdeals:
        message = f"{hotdeal['title']}"
        update.message.reply_text(message)

# 키워드 핫딜 버튼 핸들러
def keyword_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "핫딜 키워드를 입력하세요."
    update.message.reply_text(message)

# 키워드 입력 핸들러
def keyword_input_handler(update, context):
    keyword = update.message.text
    cursor = connection.cursor(dictionary=True)
    hotdeals = get_hotdeals_by_keyword(cursor, keyword)
    cursor.close()
    for deal in hotdeals:
        message = f"{deal['title']}"
        update.message.reply_text(message)

# start 명령어 함수
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 버튼 생성
    keyboard = [
        [InlineKeyboardButton("최신 핫딜", callback_data='latest_hotdeal')],
        [InlineKeyboardButton("키워드 검색", callback_data='keyword')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # 채팅방으로 버튼 전송
    await update.message.reply_text("핫딜공유방 입장을 환영합니다.\n버튼을 선택해 주세요.", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 콜백 정보 저장
    query = update.callback_query
    # 사용자가 누른 버튼의 콜백 데이터 가져오기
    await query.answer()

    # DB에서 최신 핫딜 가져오기
    cursor = connection.cursor(dictionary=True)
    hotdeals = get_latest_hotdeals(cursor)
    cursor.close()

    # 가져온 핫딜 정보를 메시지로 보내기
    hotdeal_messages = [f"{hotdeal['title']}\n\t→ {hotdeal['deal_url']}" for hotdeal in hotdeals]
    message_text = "\n".join(hotdeal_messages)
    await query.edit_message_text(text=message_text)

    # await query.edit_message_text(text=f"Selected option: {query.data}")

if __name__ == '__main__':

    # 챗봇 application 인스턴스 생성
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    # start 핸들러
    start_handler = CommandHandler('start', start)
    # start 핸들러 추가
    application.add_handler(start_handler)
    # 콜백 핸들러 추가
    application.add_handler(CallbackQueryHandler(button))
    # 폴링 방식으로 실행
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