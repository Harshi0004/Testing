import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from pymongo import MongoClient
import gridfs
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')
BOT_TOKEN = os.getenv('BOT_TOKEN')

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
fs = gridfs.GridFS(db)

notes_collection = db['notes']

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("1st Year", callback_data='1st year')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Select your year:', reply_markup=reply_markup)

async def year_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("Semester 1", callback_data='1st year-Semester 1')],
        [InlineKeyboardButton("Semester 2", callback_data='1st year-Semester 2')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Select your semester:", reply_markup=reply_markup)

async def semester_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    year, semester = query.data.split('-')
    
    subjects = notes_collection.distinct("subject", {"year": year, "branch": "CSE", "semester": semester})
    keyboard = [[InlineKeyboardButton(subject, callback_data=f'{year}-{semester}-{subject}')] for subject in subjects]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Select your subject:", reply_markup=reply_markup)

async def subject_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    year, semester, subject = query.data.split('-')
    
    note = notes_collection.find_one({"year": year, "branch": "CSE", "semester": semester, "subject": subject})
    if note:
        pdf = fs.get_last_version(note['pdf_filename'])
        await query.message.reply_document(document=pdf, filename=note['pdf_filename'], caption=f"Notes for {subject}")
    else:
        await query.edit_message_text(text="No notes found for this subject.")

def main() -> None:
    # Initialize the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(year_callback, pattern='^1st year$'))
    application.add_handler(CallbackQueryHandler(semester_callback, pattern='^1st year-Semester [1-2]$'))
    application.add_handler(CallbackQueryHandler(subject_callback, pattern='^1st year-Semester [1-2]-.+$'))

    # Start polling
    application.run_polling()

if __name__ == '__main__':
    main()
    
