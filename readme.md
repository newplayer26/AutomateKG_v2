# LLM-Powered Unstructured Data Analyzer

This Node.js web application leverages Large Language Models (LLM) to analyze unstructured data. It combines Python scripts for data processing with a Node.js server for web functionality.

## Folder Structure

```plaintext
project-root/
│
├── scripts/
│   └── (Python scripts for data processing)
│
├── server/
│   ├── node_modules/
│   ├── (JavaScript files for server logic)
│   └── package.json
│
├── .env
├── .gitignore
└── requirements.txt
```


## Prerequisites

- Node.js (version 17 or higher)
- Python (version 3.11 or higher)
- npm (usually comes with Node.js)
- pip (Python package manager)

## Installation

1. Clone the repository:


2. Install Python dependencies:

```plaintext
pip install -r requirements.txt
```

3. Install Node.js dependencies:

```plaintext
cd server
npm install
```

  

4. Set up environment variables:
- Copy the `.env.example` file to `.env`
- Fill in the required environment variables in the `.env` file

## Usage
Start the Node.js server:

```plaintext
cd server
node app.js
```

The server should now be running on `http://localhost:3000` (or your specified port)
