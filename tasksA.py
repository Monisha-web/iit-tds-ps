# task1.py



import sqlite3
import subprocess
from dateutil.parser import parse
from datetime import datetime
import json
from pathlib import Path
import os
import requests
from scipy.spatial.distance import cosine
from dotenv import load_dotenv

load_dotenv()

AIPROXY_TOKEN = os.getenv('AIPROXY_TOKEN')


def A1(email="23f2000136@ds.study.iitm.ac.in"):
    try:
        process = subprocess.Popen(
            ["uv", "run", "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py", email],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error: {stderr}")
        return stdout
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error: {e.stderr}")
# A1()
def A2(prettier_version="prettier@3.4.2", filename="/data/format.md"):
    import subprocess
    command = [r"C:\Program Files\nodejs\npx.cmd", prettier_version, "--write", filename]
    try:
        subprocess.run(command, check=True)
        print("Prettier executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def A3(filename='/data/dates.txt', targetfile='/data/dates-wednesdays.txt', weekday=2):
    input_file = filename
    output_file = targetfile
    weekday = weekday
    weekday_count = 0

    with open(input_file, 'r') as file:
        weekday_count = sum(1 for date in file if parse(date).weekday() == int(weekday)-1)


    with open(output_file, 'w') as file:
        file.write(str(weekday_count))

def A4(filename="/data/contacts.json", targetfile="/data/contacts-sorted.json"):
    # Load the contacts from the JSON file
    with open(filename, 'r') as file:
        contacts = json.load(file)

    # Sort the contacts by last_name and then by first_name
    sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))

    # Write the sorted contacts to the new JSON file
    with open(targetfile, 'w') as file:
        json.dump(sorted_contacts, file, indent=4)

def A5(log_dir_path='/data/logs', output_file_path='/data/logs-recent.txt', num_files=10):
    log_dir = Path(log_dir_path)
    output_file = Path(output_file_path)

    # Get list of .log files sorted by modification time (most recent first)
    log_files = sorted(log_dir.glob('*.log'), key=os.path.getmtime, reverse=True)[:num_files]

    # Read first line of each file and write to the output file
    with output_file.open('w') as f_out:
        for log_file in log_files:
            with log_file.open('r') as f_in:
                first_line = f_in.readline().strip()
                f_out.write(f"{first_line}\n")

def A6(doc_dir_path='/data/docs', output_file_path='/data/docs/index.json'):
    import os
    import json
    import re
    docs_dir = doc_dir_path
    index_data = {}
    
    # Regular expression to match an H1 header, allowing for leading whitespace.
    h1_regex = re.compile(r'^\s*#\s+(.*)')
    
    # Walk through all files in the docs directory.
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        match = h1_regex.match(line)
                        if match:
                            title = match.group(1).strip()
                            # Compute the relative path from docs_dir and replace backslashes with forward slashes.
                            relative_path = os.path.relpath(file_path, docs_dir).replace('\\', '/')
                            index_data[relative_path] = title
                            break  # Only the first H1 is needed.
    
    # Write the index data to the output file.
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=4)
    
    return index_data


def A7(filename='/data/email.txt', output_file='/data/email-sender.txt'):
    # Read the content of the email
    with open(filename, 'r') as file:
        email_content = file.readlines()

    sender_email = "sujay@gmail.com"
    for line in email_content:
        if "From" == line[:4]:
            sender_email = (line.strip().split(" ")[-1]).replace("<", "").replace(">", "")
            break

    # Get the extracted email address

    # Write the email address to the output file
    with open(output_file, 'w') as file:
        file.write(sender_email)

import base64
def png_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string

def A8(filename='/data/credit_card.txt', image_path='/data/credit_card.png'):
    import os
    import json
    import requests

    # Construct the request body with a clearer instruction.
    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Extract the 16-digit credit card number from this image. "
                            "The image displays a credit card number with a space after every 4 digits. "
                            "Return only the 16-digit number without any spaces or extra characters."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{png_to_base64(image_path)}"
                        }
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('AIPROXY_TOKEN')}"
    }

    # Make the request to the AIProxy service.
    response = requests.post(
        "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
        headers=headers,
        data=json.dumps(body)
    )
    response.raise_for_status()
    result = response.json()

    # Extract the card number from the response.
    card_number = result['choices'][0]['message']['content'].strip()
    # Remove any spaces if they exist.
    card_number = card_number.replace(" ", "")
    
    # Write the extracted card number to the output file.
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(card_number)
    
    return card_number



def get_embedding(text):
    api_key = os.getenv("AIPROXY_TOKEN")
    if not api_key:
        raise Exception("AIPROXY_TOKEN not set")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "text-embedding-3-small",  # or the model you intend to use
        "input": text
    }
    response = https.post("https://aiproxy.sanand.workers.dev/openai/v1/embeddings", headers=headers, json=data)
    response.raise_for_status()  # Will raise an HTTPError if status is 4xx or 5xx
    result = response.json()
    if "data" not in result:
        raise Exception("Response JSON does not contain 'data': " + json.dumps(result))
    # Extract the embedding (assuming the response data is a list with at least one element)
    embedding = result["data"][0]["embedding"]
    return embedding

def cosine(vec1, vec2):
    # Compute cosine similarity between two numpy arrays.
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 1.0
    return 1 - dot / (norm1 * norm2)

def A9(filename='/data/comments.txt', output_filename='/data/comments-similar.txt'):
    # Read comments
    with open(filename, 'r', encoding="utf-8") as f:
        comments = [line.strip() for line in f.readlines() if line.strip()]
    
    # Get embeddings for all comments
    embeddings = [get_embedding(comment) for comment in comments]
    
    # Find the most similar pair (lowest cosine distance)
    min_distance = float('inf')
    most_similar = (None, None)
    
    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            distance = cosine(embeddings[i], embeddings[j])
            if distance < min_distance:
                min_distance = distance
                most_similar = (comments[i], comments[j])
    
    # Write the most similar pair to file
    with open(output_filename, 'w', encoding="utf-8") as f:
        f.write(most_similar[0] + '\n')
        f.write(most_similar[1] + '\n')
    
    return most_similar

def A10(filename='/data/ticket-sales.db', output_filename='/data/ticket-sales-gold.txt', query="SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'"):
    # Connect to the SQLite database
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    # Calculate the total sales for the "Gold" ticket type
    cursor.execute(query)
    total_sales = cursor.fetchone()[0]

    # If there are no sales, set total_sales to 0
    total_sales = total_sales if total_sales else 0

    # Write the total sales to the file
    with open(output_filename, 'w') as file:
        file.write(str(total_sales))

    # Close the database connection
    conn.close()
