from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from rich import print

model = init_chat_model("open-mistral-7b", model_provider="mistralai", max_tokens=50)

# response = model.invoke("Hello")
# print(response.content)

print("press 1 for sad mode")
print("press 2 for angry mode")
print("press 3 for funny mode")

choice = input("Enter your choice:: ")
mode = "You are a funny AI assistant..."
if choice == 1:
    mode = "You are a sad emotional AI assistant..."
elif choice == 2:
    mode = "You are an angry AI assistant..."
elif choice == 3:
    mode = "You are a funny AI assistant..."


message = [
    SystemMessage(mode)
]
while True:
    prompt = input("user:: ")
    message.append(HumanMessage(prompt))
    if prompt in ["stop", "exit"]:
        break
    response = model.invoke(message)
    message.append(AIMessage(response.content))
    print(response.content)

print(message)
