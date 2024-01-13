# Bookkeeping Financial Manager Backend
## Overview
This backend system is designed to manage bookkeeping and financial data. It stores user information and their expenses in a PostgreSQL database, providing a set of APIs to interact with the data.

# Prerequisites
- Python 3.11
- PostgreSQL 16
- [Frontend Repository](https://github.com/AlvinLim1010/Bookkeeping-frontend)

# Installation
1. Clone the repository:
   ```
   git clone https://github.com/AlvinLim1010/Bookkeeping-API.git
   ```

2. Navigate to the project directory:
   ```
   cd Bookkeeping-API
   ```

3. Create and use the virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   
4. Install dependencies using pip:
   ```
   pip install -r requirements.txt
   ```

5. Create a new file named .env:
   <dl>
    <dt></dt>
    > copy all content in .env_sample.txt to .env   
    >  Edit the .env file with your PostgreSQL database credentials and other necessary configurations.  
    </dl>

# Configuration
Ensure that you have PostgreSQL installed and running. Update the .env file with the following information:
  ```
  DB_HOST=your_database_host
  DB_PORT=your_database_port
  DB_NAME=your_database_name
  DB_USER=your_database_user
  DB_PASSWORD=your_database_password
  SECRET_KEY=your_secret_key
  DEBUG=True
  ```

# Database Setup
Create a PostgreSQL database for the project:
- Dbeaver (recommended)
  
# Usage
Start the backend server:
```
python app.py
```

Access the API documentation at http://localhost:5000/docs/ to explore available endpoints.

# Frontend Integration
- Integrate this backend with the frontend by updating the frontend API URLs to point to your deployed backend.
- 
