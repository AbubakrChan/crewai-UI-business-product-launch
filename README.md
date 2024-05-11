# Streamlit UI for crewai

### Prerequisites

Before proceeding, ensure you have the following installed on your system:

- Python (version 3.10 or higher)
- pip (Python package installer)

### Installation Steps

1. **Clone the Repository:**
   
   Clone the project repository to your local machine using Git by running the following command in your terminal or command prompt:

   ```
   git clone https://github.com/AbubakrChan/crewai-business-product-launch.git
   ```

2. **Navigate to Project Directory:**
   
   Change your working directory to the project directory using the following command:

   ```
   cd crewai-business-product-launch
   ```

3. **Install Dependencies:**
   
   Install the required Python dependencies listed in the `requirements.txt` file using pip. Run the following command:

   ```
   pip install -r requirements.txt
   ```
4. **Set Up OpenAI API Key:**

   To utilize the OpenAI API within the application, ensure you have an OpenAI API key. Set your OpenAI API key as an environmental variable named OPENAI_API_KEY on your system.
   
   Create a .env file in the project directory if it doesn't exist already. Add the following line to the .env file, replacing sk-xxxxxxxxxxxxxxxxx with your actual OpenAI API key:
   
   ```
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxx
   ```
   
### Running the Streamlit Application

Once you've completed the setup steps, you can run the Streamlit application using the following command:

```
streamlit run main.py
```

This command will launch the application, and you should see the URL where the app is running. Typically, it will be something like `http://localhost:8501`.

### Usage

- Upon running the Streamlit application, you will be presented with the interface of the CrewAI Business Product Launch.
  
## Demo: 
https://www.loom.com/share/ab57dc1585804b7a86cc8a8315d9d294
