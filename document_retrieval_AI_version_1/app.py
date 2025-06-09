from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
import re
import shutil
from PyPDF2 import PdfReader
from typing import List, Dict
import json
from werkzeug.utils import secure_filename
import tempfile
import zipfile
from datetime import datetime
from openai import OpenAI
import openai
import dotenv
import os
from pathlib import Path

# Set environment variable manually
os.environ["OPENAI_API_KEY"] = "your own api"
openai.api_key = os.environ["OPENAI_API_KEY"]

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Get OpenAI API key from environment variable
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs('database', exist_ok=True)

# Store PDF content in memory for chat context
pdf_content_cache = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")
    return text

def find_required_documents(text: str) -> List[str]:
    """
    Identify required documents mentioned in the text.
    Looks for common document types like certificates, reports, etc.
    """
    # Common document patterns to look for
    patterns = [
        r'\b(certificate[s]?|cert[s]?)\b',
        r'\b(audit report[s]?)\b',
        r'\b(organization[s]?|org[s]?)\b',
        r'\b(report[s]?)\b',
        r'\b(statement[s]?)\b',
        r'\b(license[s]?|licence[s]?)\b',
        r'\b(permit[s]?)\b',
        r'\b(registration[s]?)\b',
        r'\b(contract[s]?)\b',
        r'\b(agreement[s]?)\b',
        r'\b(reference[s]?)\b',
        r'\b(brochure[s]?)\b',
        r'\b(catalogue[s]?)\b',
        r'\b(datasheet[s]?)\b',
        r'\b(document[s]?)\b',
        r'\b(copy[s]?)\b',
        r'\b(copies[s]?)\b',
        r'\b(profile[s]?)\b',
        r'\b(experience[s]?)\b',
        r'\b(plan[s]?)\b',
        r'\b(cover[s]?)\b',
        r'\b(iso[s]?)\b'
    ]
    
    required_docs = set()
    
    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        for match in matches:
            # Handle tuple matches (from capture groups)
            if isinstance(match, tuple):
                match = next(m for m in match if m)
            required_docs.add(match.lower())
    
    return list(required_docs)

def search_matching_pdfs(search_folders: List[str], required_docs: List[str]) -> Dict[str, List[str]]:
    """
    Search through folders for PDFs that match the required documents.
    Returns a dictionary mapping document types to found PDF paths.
    """
    doc_matches = {doc: [] for doc in required_docs}
    
    for folder in search_folders:
        if not os.path.exists(folder):
            print(f"Warning: Folder {folder} does not exist")
            continue
            
        for root, _, files in os.walk(folder):
            for file in files:
                if file.lower().endswith('.pdf') or file.lower().endswith('.docx'):
                    file_lower = file.lower()
                    for doc in required_docs:
                        # Check if document type is mentioned in filename
                        if doc in file_lower:
                            full_path = os.path.join(root, file)
                            doc_matches[doc].append(full_path)
    
    return doc_matches

def copy_matching_pdfs(doc_matches: Dict[str, List[str]], output_folder: str) -> tuple:
    """
    Copy matching PDFs to the output folder.
    Returns the number of files copied and list of copied files.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    count = 0
    copied_files = []
    
    for doc_type, file_paths in doc_matches.items():
        for i, src_path in enumerate(file_paths):
            filename = os.path.basename(src_path)
            # Handle duplicate filenames
            if i > 0:
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{i}{ext}"
            dst_path = os.path.join(output_folder, filename)
            
            try:
                shutil.copy2(src_path, dst_path)
                count += 1
                copied_files.append({
                    'original_path': src_path,
                    'copied_path': dst_path,
                    'filename': filename,
                    'doc_type': doc_type
                })
                print(f"Copied: {filename} (matches '{doc_type}')")
            except Exception as e:
                print(f"Error copying {src_path}: {e}")
    
    return count, copied_files

def ask_chatgpt(question: str, pdf_content: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Ask ChatGPT a question about the PDF content using the new OpenAI API (1.0.0+).
    """
    if not OPENAI_API_KEY:
        return "Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."
    
    try:
        # Truncate PDF content if it's too long (to fit within token limits)
        max_content_length = 14000  # Approximate token limit for context
        if len(pdf_content) > max_content_length:
            pdf_content = pdf_content[:max_content_length] + "...[content truncated]"
        
        # Create system message with instructions
        system_message = """
        You are an assistant that helps users understand PDF documents. 
        Answer questions based on the PDF content provided. 
        If the answer is not in the PDF content, say so clearly.
        Be concise and specific in your answers.
        """
        
        # Create messages for the API call
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"PDF Content:\n\n{pdf_content}\n\nQuestion: {question}"}
        ]
        
        # Call the OpenAI API using the new client format
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=500,
            temperature=0.3,
        )
        
        # Extract and return the response
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Flask server is running!'})

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        print("Received upload request")
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        search_folders = request.form.get('search_folders', 'database').split(',')
        search_folders = [folder.strip() for folder in search_folders if folder.strip()]
        output_folder = request.form.get('output_folder', 'output')
        
        print(f"File: {file.filename}")
        print(f"Search folders: {search_folders}")
        print(f"Output folder: {output_folder}")
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print(f"File saved to: {filepath}")
            
            # Process the PDF
            try:
                # Step 1: Extract text from PDF
                print("Extracting text from PDF...")
                pdf_text = extract_text_from_pdf(filepath)
                print(f"Extracted {len(pdf_text)} characters")
                
                # Store PDF content in cache for chat functionality
                pdf_content_cache[filename] = pdf_text
                
                # Step 2: Find required documents
                print("Finding required documents...")
                required_docs = find_required_documents(pdf_text)
                print(f"Found document types: {required_docs}")
                
                if not required_docs:
                    return jsonify({
                        'error': 'No document requirements found in the PDF',
                        'extracted_text': pdf_text[:500] + '...' if len(pdf_text) > 500 else pdf_text
                    }), 400
                
                # Step 3: Search for matching files
                print("Searching for matching files...")
                doc_matches = search_matching_pdfs(search_folders, required_docs)
                print(f"Found matches: {doc_matches}")
                
                # Step 4: Copy matching files
                print("Copying matching files...")
                total_copied, copied_files = copy_matching_pdfs(doc_matches, output_folder)
                print(f"Copied {total_copied} files")
                
                # Prepare response
                matches = []
                for doc_type, file_paths in doc_matches.items():
                    if file_paths:  # Only include document types that have matches
                        matches.append({
                            'type': doc_type,
                            'files': [os.path.basename(path) for path in file_paths]
                        })
                
                response = {
                    'success': True,
                    'required_docs': required_docs,
                    'matches': matches,
                    'total_copied': total_copied,
                    'output_folder': output_folder,
                    'copied_files': copied_files,
                    'filename': filename  # Include filename for chat reference
                }
                
                return jsonify(response)
                
            except Exception as e:
                # Clean up uploaded file on error
                if os.path.exists(filepath):
                    os.remove(filepath)
                print(f"Processing error: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
        
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    """Download processed files"""
    try:
        # Security: only allow downloads from output folder
        safe_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(safe_path):
            return send_file(safe_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/chat', methods=['POST'])
def chat():
    """Chat with GPT about PDF content"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        question = data.get('question')
        filename = data.get('filename')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400
        
        # Get PDF content from cache
        pdf_content = pdf_content_cache.get(filename)
        if not pdf_content:
            return jsonify({'error': 'PDF content not found. Please upload the file again.'}), 404
        
        # Ask ChatGPT
        response = ask_chatgpt(question, pdf_content)
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': response
        })
        
    except Exception as e:
        print(f"Chat error: {str(e)}")
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/api-key-status')
def api_key_status():
    """Check if OpenAI API key is configured"""
    if OPENAI_API_KEY:
        return jsonify({'configured': True})
    else:
        return jsonify({'configured': False})

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Server will be available at: http://localhost:5000")
    print(f"Make sure you have the following folders:")
    print(f"  - {UPLOAD_FOLDER}/ (for temporary uploads)")
    print(f"  - database/ (put your searchable documents here)")
    print(f"  - {OUTPUT_FOLDER}/ (for processed results)")
    
    if not OPENAI_API_KEY:
        print("\n⚠️ WARNING: OpenAI API key not found!")
        print("To use the ChatGPT feature, please set your API key:")
        print("  1. Create a .env file in the project directory")
        print("  2. Add this line: OPENAI_API_KEY=your_api_key_here")
        print("  3. Restart the server")
    else:
        print("\n✅ OpenAI API key configured successfully!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
