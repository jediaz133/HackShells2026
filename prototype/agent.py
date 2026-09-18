import os, base64, json, time, math
from langchain_core.tools import tool
from langgraph.runtime import get_runtime
from langchain.agents import create_agent
from ollama import chat
from dataclasses import dataclass
from tools import *
import datetime, json, os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = ""
os.environ["NO_PROXY"] = "localhost,127.0.0.1"
os.environ["LANGSMITH_TRACING"]="false"
os.environ["OLLAMA_BASE_URL"]="http://localhost:11434"

systemFile = open("Setting.system", "r+")
system = systemFile.read()
systemFile.close()

# @dataclass
# class RuntimeContext:
#     simu: client
tools = [
    userEdit,
    userRead,
    getTime,
    logDay,
    checkDates,
    getDayData,
    editDay,]

# agent = create_agent(

#     # Our gemma model
#     model="ollama:hf.co/unsloth/gemma-4-E4B-it-qat-GGUF:UD-Q4_K_XL",
#     tools=tools,
#     system_prompt=system,
#     # context_schema=RuntimeContext,
# )


currentRequest = False


gemini = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

agent = create_agent(
    model=gemini,
    tools=tools,
    system_prompt=system)


def askAI(question):
    content = ""
    if os.path.isfile("image.jpg"):
        content = { "messages": 
                    {"role": "user", 
                     "content": [
                                {"type": "text",
                                "text": question,},
                                {"type": "image_url", 
                                 "image_url": {
                                                "url": f"data:image/jpeg;base64,{base64.b64encode( open("image.jpg", "rb").read()).decode("utf-8")}"
                                                }}
                                                ]}}
        os.remove("image.jpg")
    else:
        content = {"messages": question}


    # Read the stream
    for chunk in agent.stream(
        input =  content,
        stream_mode="values",
    ):
        message = chunk["messages"][-1]
        chunk["messages"][-1].pretty_print()
        content = message.content
        
        # Handle cases where the content is a list (Tool calls, Gemini blocks)
        if isinstance(content, list):
            text_parts = []
            for item in content:
                # Extract text if it's a dictionary
                if isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])
                # Extract text if it's already a string inside the list
                elif isinstance(item, str):
                    text_parts.append(item)
            
            yield "".join(text_parts)

        # Handle cases where the content is a normal string
        elif isinstance(content, str):
            yield content    
            currentRequest = False
            
    


# askAI("tell me details about my health")
