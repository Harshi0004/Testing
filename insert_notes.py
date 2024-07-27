import os
import gridfs
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI and database name from environment variables
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
fs = gridfs.GridFS(db)

def upload_pdf(file_path, file_name):
    with open(file_path, 'rb') as f:
        fs.put(f, filename=file_name)

# List of PDF files to upload
pdf_files = [
    {"file_path": "pdfs/notes_sem1_lac.pdf", "file_name": "notes_sem1_lac.pdf"},
    {"file_path": "pdfs/notes_sem1_physics.pdf", "file_name": "notes_sem1_physics.pdf"},
    {"file_path": "pdfs/notes_sem1_c.pdf", "file_name": "notes_sem1_c.pdf"},
    {"file_path": "pdfs/notes_sem1_beee.pdf", "file_name": "notes_sem1_beee.pdf"},
    {"file_path": "pdfs/notes_sem2_ps.pdf", "file_name": "notes_sem2_ps.pdf"},
    {"file_path": "pdfs/notes_sem2_chemistry.pdf", "file_name": "notes_sem2_chemistry.pdf"},
    {"file_path": "pdfs/notes_sem2_python.pdf", "file_name": "notes_sem2_python.pdf"},
    {"file_path": "pdfs/notes_sem2_english.pdf", "file_name": "notes_sem2_english.pdf"},
]

# Upload each PDF file
for pdf in pdf_files:
    upload_pdf(pdf["file_path"], pdf["file_name"])

print("PDFs uploaded successfully!")
