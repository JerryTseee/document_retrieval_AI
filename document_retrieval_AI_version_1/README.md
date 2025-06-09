# Document Retrieval AI
It is a web-base AI tool that can help you to retrieve the required documents from the database according to your uploaded pdf file. It also supports some AI chatbot functions.

## V0.dev 
*Automatically synced with your [v0.dev](https://v0.dev) deployments*

[![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=for-the-badge&logo=vercel)](https://vercel.com/bpsaitools-5647s-projects/v0-pdf-document-processor)
[![Built with v0](https://img.shields.io/badge/Built%20with-v0.dev-black?style=for-the-badge)](https://v0.dev/chat/projects/cgxGwO6hZdI)

This repository will stay in sync with your deployed chats on [v0.dev](https://v0.dev).
Any changes you make to your deployed app will be automatically pushed to this repository from [v0.dev](https://v0.dev).

## Deployment

project is live at:

**[https://vercel.com/bpsaitools-5647s-projects/v0-pdf-document-processor](https://vercel.com/bpsaitools-5647s-projects/v0-pdf-document-processor)**

## Quick Setup

## Build your app

Continue building your app on:

**[https://v0.dev/chat/projects/cgxGwO6hZdI](https://v0.dev/chat/projects/cgxGwO6hZdI)**

1. Create and modify your project using [v0.dev](https://v0.dev)
2. Deploy your chats from the v0 interface
3. Changes are automatically pushed to this repository
4. Vercel deploys the latest version from this repository


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