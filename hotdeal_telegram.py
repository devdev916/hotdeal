from telegram import Bot
import mysql.connector
import asyncio
# import schedule


# telegram 연결 설정 
TELEGRAM_BOT_TOKEN = '6417926677:AAFpFVg4zGjjytISsI7h5qsg6QHIEophjqc'
TELEGRAM_CHAT_ID = '7090041263'
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_hotdeal(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM deals")
    deals = cursor.fetchall()
    cursor.close()

    for deal in deals:
        message = f'''{deal['title']}'''
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

if __name__ == "__main__":
    # MySQL 연결 설정
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0916",
        database="hotdeal"
    )

    # 데이터베이스에서 정보 가져와서 메시지 보내기
    asyncio.run(send_hotdeal(connection))

    # MySQL 연결 종료
    connection.close()