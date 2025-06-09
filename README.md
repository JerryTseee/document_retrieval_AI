## Document Retrieval AI
It is a web-base AI tool that can help you to retrieve the required documents from the database according to your uploaded pdf file. It also supports some AI chatbot functions.

## User Interface
![image](https://github.com/user-attachments/assets/490c2707-4b9a-4108-bbe1-050515f55ed0)
![image](https://github.com/user-attachments/assets/aaca2f95-fc0a-413f-a596-cb0a56392973)


## Folder Structure
\`\`\`
your-project/
├── app.py                          # Flask backend server
├── index.html                      # Web interface
├── upload your pdf file/           # Temporary uploaded files
├── database/                       # Put your searchable documents here
└── output folder/                  # Processed results appear here
\`\`\`

## Steps:
1. create a virtual environment
2. pip install -r requirement.txt
3. pip install openai
4. pip install dotenv
5. run app.py
6. open browser then : http://localhost:5000
7. you can use the app now!

## Usage
1. Put your searchable PDF/DOCX files in the `database` folder
2. Start the Flask server: `python app.py`
3. Open http://localhost:5000 in your browser
4. Upload a PDF containing document requirements
5. Configure search folders and output location
6. Click "Start Processing"
7. Download results from the output folder
