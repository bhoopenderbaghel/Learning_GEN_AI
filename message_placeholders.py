from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage,AIMessage
#chat template 
chat_template = ChatPromptTemplate([
    ('system','you are a helpful customer support agent'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human','{query}')
])

chat_history = []
#load chat hisory 
with open('chat_history.txt') as f:
 for line in f:
        line = line.strip()
        if line.startswith("HumanMessage"):
            content = line.split('content="')[1].rstrip('")')
            chat_history.append(HumanMessage(content=content))
        elif line.startswith("AIMessage"):
            content = line.split('content="')[1].rstrip('")')
            chat_history.append(AIMessage(content=content))

print(chat_history)
#create prompt

prompt = chat_template.invoke({
    'chat_history': chat_history,
    'query': 'Where is my refund?'
})

print(prompt)