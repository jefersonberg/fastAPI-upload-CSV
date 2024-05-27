import chardet
from typing import List
from fastapi import UploadFile, HTTPException
from app.db.mongodb import get_database
from io import BytesIO
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.services.rabbit_service import batch_publish_to_queue

def detect_encoding(file: BytesIO, sample_size: int = 1024) -> str:
    # Read a sample of the file to detect the encoding
    sample = file.read(sample_size)
    result = chardet.detect(sample)
    file.seek(0)  # Reset the file pointer to the beginning
    return result['encoding']

def save_to_db(data_chunk: List[dict]):
    db = get_database()
    collection = db["debts"]
    collection.insert_many(data_chunk)

async def process_csv(file: UploadFile):

    # Read the content of the CSV file
    content = await file.read()
    file_like = BytesIO(content)

    # Detect the encoding of the CSV file
    encoding = detect_encoding(file_like)

    # Define the chunk size
    chunk_size = 10000

    try:
        # Read and process the CSV in chunks
        chunks = pd.read_csv(file_like, chunksize=chunk_size, encoding=encoding)

        with ThreadPoolExecutor() as executor:
            futures = []
            for chunk in chunks:
                chunk['debtDueDate'] = pd.to_datetime(chunk['debtDueDate'], errors='coerce')
                data_chunk = chunk.to_dict(orient='records')

                # Save records to MongoDB
                futures.append(executor.submit(save_to_db, data_chunk))

                # Save records to RabbitMQ
                # futures.append(executor.submit(batch_publish_to_queue, 'email_queue', data_chunk))

            # Wait for all futures to complete
            for future in as_completed(futures):
                future.result()

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing the CSV file: {str(e)}")

    return {"message": "File processed successfully"}
