# 🍲 Kitchen Grocery Assistant

A **Chainlit-based chatbot** that helps you check your kitchen stock.  
It supports **English** and **Roman Urdu** responses and sends **email notifications** for each interaction.

---

## 🧩 Features
- Predefined, fixed kitchen stock (user **cannot modify** it)  
- Multi-language support: English & Roman Urdu  
- Email notifications for every chat interaction  
- Web-based chat using **Chainlit UI**  
- Smart replies using **Google Gemini AI**

---

## 🛠️ Tech Stack
- Python 3.11+  
- Chainlit  
- AsyncOpenAI (Gemini-compatible)  
- `dotenv` for environment variables  
- `smtplib` & `EmailMessage` for notifications

---

## 📦 Kitchen Stock
The chatbot can answer queries for items like:

- **Basics:** Flour, Rice, Sugar, Oil, Lentils…  
- **Vegetables:** Onion, Tomato, Potato…  
- **Meat & Dairy:** Chicken, Beef, Eggs, Milk…  
- **Drinks & Snacks:** Tea, Juice, Biscuits…  
- **Sauces & Dry Fruits:** Ketchup, Almonds, Cashews…  
- **Frozen Food:** Frozen paratha, Ice cream…  

> **Note:** The stock is fixed and does not update based on user input.

---

## ⚡ Installation

```bash
git clone https://github.com/username/kitchen-agent.git
cd kitchen-agent
python -m venv .venv

# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
Create a .env file with your credentials:

ini
Copy code
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
GEMINI_API_KEY=your_gemini_api_key
🚀 Run Locally
bash
Copy code
chainlit run main.py
Open your browser at http://localhost:8000 (or the link provided by Chainlit).

📧 Email Notifications
Every message sent by the user triggers an email to your EMAIL_USER containing both the user query and the assistant’s response.

🤖 Usage
Ask questions like:

How much rice do I have?

Mere paas 2 kilo sugar h?

The bot will reply with the correct stock from the predefined list.

🌐 Live Demo
Kitchen Agent on Vercel

📚 Resources
GitHub Repository: https://github.com/username/kitchen-agent

Tech Stack: Python, Chainlit, Gemini AI











