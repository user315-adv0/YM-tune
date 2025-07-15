import os
from dotenv import load_dotenv

load_dotenv()

YA_TOKEN = os.getenv("YA_TOKEN")
if not YA_TOKEN:
    print("⚠️  YA_TOKEN не найден в .env файле!")
    print("Создайте backend/.env с YA_TOKEN=your_token_here") 