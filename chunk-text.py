import re
import json
import os
import chardet

# Here i am looking at encoding of the file
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        return result['encoding']

# This is where I chunk the file and put the conditions for minimum and maximum chunks
def chunk_text_file(file_path, token_limit=400, max_token_limit=500):
    # I added this piece to detect the encoding of the file automatically
    encoding = detect_encoding(file_path)
    print(f"Detected encoding: {encoding}")

    # Open the file with the detected encoding, handle errors by replacing invalid characters
    with open(file_path, 'r', encoding=encoding, errors='replace') as file:
        text = file.read()

    # On this function I am tokenizing the text (assuming tokens are words split by spaces)
    tokens = text.split()

    chunks = []
    current_chunk = []
    token_count = 0

    # In this part I am iterating over the tokens and create chunks
    for token in tokens:
        current_chunk.append(token)
        token_count += 1

        # Here I am doing a max token check on each chunk.
        if token_count >= token_limit and re.search(r'\.\s$', token):
            # Here i am combining the chunk and store it
            chunks.append(' '.join(current_chunk))
            # Once I store, the following step will setup the iteration for the next chunk
            current_chunk = []
            token_count = 0
        
        # Here i am forcing a chunk if I pass 450 tokens and hit 500 without seeing a period and a space.
        elif token_count >= max_token_limit:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            token_count = 0

    # This part just adds any remaining tokens in the last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Function to save chunks to JSON files in a specified directory
def save_chunks_to_json(file_path, chunks, output_directory):
    # Here is where I create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    document_name = file_path.split('/')[-1]  # Extract the file name from the path

    for i, chunk in enumerate(chunks):
        chunk_data = {
            "original_document": document_name,
            "chunk_number": i + 1,
            "body": chunk
        }
        # Save each chunk as a separate JSON file
        json_output_file = os.path.join(output_directory, f"{document_name.split('.')[0]}_chunk_{i+1}.json")
        with open(json_output_file, 'w', encoding='utf-8') as json_file:
            json.dump(chunk_data, json_file, ensure_ascii=False, indent=4)

    print(f"Chunks have been saved in JSON format to directory: {output_directory}")

# Example usage
file_path = 'File_Path_Here'  # Replace this with your file path
output_directory = 'Output_directory_here'  # Replace with the desired output directory

# Run the chunking process
chunks = chunk_text_file(file_path)

# Save the chunks to JSON files in the specified directory
save_chunks_to_json(file_path, chunks, output_directory)
