import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # Simple chatbot reply
    await cl.Message(
        content=f"👋 Hello! Tumne bola: {message.content}"
    ).send()
