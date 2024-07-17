# LLM-Powered Unstructured Data Analyzer

This Node.js web application leverages Large Language Models (LLM) to analyze unstructured data. It combines Python scripts for data processing with a Node.js server for web functionality.

## Folder Structure
project-root/
│
├── scripts/
│ └── (Python scripts for data processing)
│
├── server/
│ ├── node_modules/
│ ├── (JavaScript files for server logic)
│ └── package.json
│
├── .env
├── .gitignore
└── requirements.txt


## Prerequisites

- Node.js (version 17 or higher)
- Python (version 3.11 or higher)
- npm (usually comes with Node.js)
- pip (Python package manager)

## Installation

1. Clone the repository:

2. Install Node.js dependencies:
cd server
npm install

3. Install Python dependencies:
pip install -r requirements.txt
sql_more
Copy

4. Set up environment variables:
- Copy the `.env.example` file to `.env`
- Fill in the required environment variables in the `.env` file

## Usage

1. Start the Node.js server:
cd server
npm start
Copy

2. The server should now be running on `http://localhost:3000` (or your specified port)
