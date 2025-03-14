# Elinity_Assignment
Flask API and LLM based Recommendation System

 


## Please see the Demo video 
[![Watch the video](https://img.youtube.com/vi/OjKQF2fnEEg/0.jpg)](https://youtu.be/OjKQF2fnEEg)


##  Inside the `Elinity` Folder
The project contains the following files:

- **`Q1.py`** → Solves User Story 1  
- **`Q2.py`** → Solves User Story 2 (Finding Similar Mindset Users using LLM - `Llama 3.2:70B`)  
- **`persona.py`** → Contains 10 example personas as mentioned in the question  
- **`curl.txt`** → Includes cURL commands for API testing  

### **Install Dependencies**
Run the following command to install all necessary packages:  

pip install -r requirements.txt

To execute Q1.py, follow these steps:

Open Visual Studio Code (VS Code) or any other IDE.
Run the script using:

# python Q1.py
API endpoints can be tested using the commands in curl.txt.
Alternatively, you can use Postman for API testing.

To execute Q2.py, follow these steps:

Check API Key: Ensure that the Together AI API key is set in .env and is working.
If the API key is not working, create a new one from Together AI and update .env.
Run the script using:

# python Q2.py
Once the server starts, you will see output similar to:

# Running on local URL: http://127.0.0.1:7860
Open the URL in a browser to access the Gradio interface and ask queries.


# Note I am uisng 10 example for now as mentioned in the Question   which is in persona.py file 







