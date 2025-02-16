# Phase B: LLM-based Automation Agent for DataWorks Solutions

# B1 & B2: Security Checks
import os
import httpx

def B12(filepath):
    if filepath.startswith('/data'):
        # raise PermissionError("Access outside /data is not allowed.")
        # print("Access outside /data is not allowed.")
        return True
    else:
        return False

# B3: Fetch Data from an API
def B3(url, save_path):
    if not B12(save_path):
        raise PermissionError("Output file must be under /data.")
    import httpx
    response = httpx.get(url)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(response.text)



def B4(repo_url, target_dir, filename, commit_message, filecontent):
    # Ensure /data exists
    os.makedirs("/data", exist_ok=True)
    # Remove "file://" prefix if present
    if repo_url.startswith("file://"):
        repo_url = repo_url[len("file://"):]
    # Ensure the target directory is under /data
    if not os.path.abspath(target_dir).startswith(os.path.abspath("/data")):
        raise PermissionError("Target directory must be under /data.")
    # Clone the repository into the target directory
    subprocess.run(["git", "clone", repo_url, target_dir], check=True)
    # Verify clone was successful by checking for the .git directory
    git_dir = os.path.join(target_dir, ".git")
    if not os.path.exists(git_dir):
        raise Exception("Clone failed: .git directory not found in target directory.")
    # Create the new file in the cloned repository
    file_path = os.path.join(target_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(filecontent)
    # Stage and commit the new file
    subprocess.run(["git", "-C", target_dir, "add", filename], check=True)
    subprocess.run(["git", "-C", target_dir, "commit", "-m", commit_message], check=True)

def B5(db_path, query, output_filename):
    # Ensure both the database and output file are under /data.
    if not (B12(db_path) and B12(output_filename)):
        raise PermissionError("Both database and output file must be under /data.")
    import sqlite3, duckdb
    # Use sqlite3 if the database ends with '.db', else duckdb.
    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    # Extract the numeric value from the result (assumes result is a list of tuples).
    if result and result[0]:
        value = result[0][0]
    else:
        value = ""
    with open(output_filename, 'w', encoding="utf-8") as file:
        file.write(str(value))
    return value



# B6: Web Scraping
def B6(url, output_filename):
    import requests
    result = requests.get(url).text
    with open(output_filename, 'w') as file:
        file.write(str(result))

# B7: Image Processing
def B7(image_path, output_path, resize=None):
    from PIL import Image
    # Enforce that both image_path and output_path are under /data.
    if not (B12(image_path) and B12(output_path)):
        raise PermissionError("Both image and output paths must be under /data.")
    try:
        with Image.open(image_path) as img:
            if resize:
                img = img.resize(resize)
            img.save(output_path)
    except Exception as e:
        raise Exception(f"Error processing image: {e}")



def B8(audio_path, output_path):
    from pathlib import Path
    # Enforce that both audio_path and output_path are under /data.
    if not (B12(audio_path) and B12(output_path)):
        raise PermissionError("Audio file and output file must be under /data.")
    
    audio_file = Path(audio_path)
    out_file = Path(output_path)
    
    # Ensure the output directory exists.
    out_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Simulate transcription by reading the audio file as text.
        transcript = audio_file.read_text(encoding="utf-8")
    except Exception as e:
        raise Exception(f"Error reading audio file {audio_path}: {e}")
    
    try:
        out_file.write_text(transcript, encoding="utf-8")
    except Exception as e:
        raise Exception(f"Error writing transcript to {output_path}: {e}")
    
    print("DEBUG: Transcript written to:", out_file.resolve())
    return transcript




# B9: Markdown to HTML Conversion
def B9(md_path, output_path):
    import markdown
    if not B12(md_path):
        return None
    if not B12(output_path):
        return None
    with open(md_path, 'r') as file:
        html = markdown.markdown(file.read())
    with open(output_path, 'w') as file:
        file.write(html)

# B10: API Endpoint for CSV Filtering
def B10(csv_path, filter_column, filter_value, output_path):
    import pandas as pd
    from pathlib import Path

    # Ensure both the CSV file and output file are under /data.
    if not (B12(csv_path) and B12(output_path)):
        raise PermissionError("CSV file or output file not under /data.")
    
    csv_file = Path(csv_path)
    out_file = Path(output_path)
    
    # Ensure the directory for the output file exists.
    out_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Read the CSV file.
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        raise Exception(f"Error reading CSV file {csv_file}: {e}")
    
    # Filter rows where filter_column equals filter_value (as a string).
    filtered = df[df[filter_column] == str(filter_value)]
    json_output = filtered.to_json(orient="records")
    
    # Write the JSON output using pathlib's write_text method.
    out_file.write_text(json_output, encoding="utf-8")
    
    # Debug: Print the absolute path and whether the file exists.
    debug_path = out_file.resolve()
    print("DEBUG: Output file absolute path:", debug_path)
    print("DEBUG: Does output file exist?", out_file.exists())
    print("DEBUG: Filtered JSON output:", json_output)
    
    return json_output


