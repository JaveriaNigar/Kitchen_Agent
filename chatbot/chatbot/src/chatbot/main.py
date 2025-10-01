import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os
import random
import smtplib
from email.message import EmailMessage

# Load environment variables
load_dotenv()
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")
api_key = os.getenv("GEMINI_API_KEY")  

# Setup Gemini-compatible client
external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# RunConfig for agent
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# --- FIXED Kitchen Stock with Consistent Units ---
kitchen_stock = {
    # Basics 
     "flour": "10 kg", 
     "rice": "8 kg", 
     "sugar": "3 kg", 
     "oil": "5 liters", 
     "salt": "1 kg", 
     "lentils": "4 kg", 
     "spices": "2 packets", 
     "chili": "500 g", 
     "turmeric": "250 g", 
     "garam masala": "200 g",
      
      
     # Vegetables 
     "onion": "4 kg", 
     "tomato": "3 kg", 
     "potato": "6 kg", 
     "vegetables": "10 kg mixed",
     
      
     # Meat & Dairy 
      "chicken": "3 kg", 
      "beef": "2 kg", 
      "mutton": "1.5 kg", 
      "fish": "1 kg", 
      "meat": "2 kg", 
      "eggs": "12 pieces", 
      "yogurt": "2 kg", 
      "milk": "5 liters", 
      
      
      # Drinks & Snacks 
      "tea": "500 g", 
      "biscuits": "3 packs", 
      "bread": "2 loaves", 
      "fruits": "5 kg mixed", 
      "chips": "5 packs", 
      "juice": "3 liters", 
      "soft drinks": "6 bottles",
      
      
      # Sauces & Condiments 
      "ketchup": "1 bottle", 
      "mayonnaise": "1 jar", 
      "soy sauce": "1 bottle",
      
      
      # Dry fruits 
      "almonds": "500 g", 
      "cashews": "250 g", 
      "raisins": "200 g", 
      "dates": "1 kg", 
      
      
      # Frozen food 
      "frozen paratha": "2 packs", 
      "frozen nuggets": "1 pack", 
      "ice cream": "2 liters" 
     }

# Kitchen Grocery Assistant Agent
agent = Agent(
    name="Kitchen Grocery Assistant",
    instructions=f"""
    You are a Kitchen Grocery Assistant.

    Responsibilities:
    - The kitchen stock is fixed and predefined. Do not update it from user input.
    - Always check the predefined stock list when the user asks.
    - If the user says something different about the stock, politely correct them with the actual value.
    - If the user speaks in English, reply in English.
    - If the user speaks in Roman Urdu, reply in Roman Urdu.
    - Do not use any other language.

    Predefined Kitchen Stock:
    {kitchen_stock}

    Examples:
    User: "How much rice do I have?"
    Reply: "You currently have 8 kg rice in your kitchen."

    User: "Mere paas 3 kilo atta h"
    Reply: "Nahi bhai, tumhare kitchen me 10 kg flour h."
    """,
    model=model
)

# --- Terminal Test ---
if __name__ == "__main__":
    user_query = input("🛒 Ask about your kitchen stock: ")
    result = Runner.run_sync(agent, user_query, run_config=config)
    print("\n📦 Kitchen Assistant Suggestion:\n", result.final_output)

# --- Function to send email notifications ---
def send_email_notification(user_message, assistant_message):
    msg = EmailMessage()
    msg.set_content(f"User: {user_message}\nAssistant: {assistant_message}")
    msg['Subject'] = "New Kitchen Agent Interaction"
    msg['From'] = email_user
    msg['To'] = email_user
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)

# --- Chainlit UI ---
@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    intro_messages = [
        "👋 Hi! I am your Kitchen Grocery Assistant.\n\nAsk me about your kitchen stock anytime!",
        "🛒 Salaam! Kitchen Assistant yahan h, tumhe apne kitchen ka stock check karna h to pooch lo.",
        "🍲 Hello! Ready to help you with your kitchen stock. Try asking me something like:\n'How much sugar do I have?'"
    ]
    intro_message = random.choice(intro_messages)
    await cl.Message(content=intro_message).send()
    
@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})

    # Run agent first
    result = Runner.run_sync(agent, message.content, run_config=config)
    assistant_reply = result.final_output

    # Send email notification with both user and assistant messages
    send_email_notification(message.content, assistant_reply)

    # Send assistant reply to user
    await cl.Message(content=assistant_reply).send()

    history.append({"role": "assistant", "content": assistant_reply})
    cl.user_session.set("history", history)
