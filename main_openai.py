

from dotenv import load_dotenv
import os
import json
from openai import OpenAI
from ddgs import DDGS

#API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

openai_client = OpenAI(api_key=api_key)

#Search function
def search_web(query):
    with DDGS() as ddgs: 
     results = ddgs.text(query, max_results=3)
    return str(results)

#IP cv, account attacks
def read_honeypot_log():
   with open("ip_time.csv", "r") as file:
      return file.read()

#Top usernames
def read_username_log():
   with open("username_ip.csv", "r") as file:
      return file.read()

#Menu
tools = [
    {
        "type": "function",
        "function": {
            "name" : "search_web",
            "description": "Search the web for current information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
       "type": "function",
       "function": {
          "name" : "read_honeypot_log",
          "description" : "Read the log of failed login attempts from my Azure honeypot project, including IPs adresses and attacker count and countries",
          "parameters" : {
             "type": "object",
             "properties" : {},
             "required" : []
          }
       }
    },
    {
       "type": "function",
       "function" : {
          "name" : "read_username_log",
          "description" : "Read the log of usernames that were attempted from my Azure honetpot project, including IPs, usernames and countries",
          "parameters": {
             "type": "object",
             "properties" : {},
             "required": []
          }
       }
    }
]


prompt = input("Ask anything!\n")
messages = [{"role": "user", "content": prompt}]

#3 first call with tools
response = openai_client.chat.completions.create(
    model="gpt-5",
    messages=messages,
    tools=tools
)

message=response.choices[0].message

#4 check to see if it used the tools
if message.tool_calls:
    messages.append(message) 

    for tool_call in message.tool_calls:
        if tool_call.function.name == "search_web":
           args = json.loads(tool_call.function.arguments)
           result = search_web(args["query"])
        elif tool_call.function.name == "read_honeypot_log":
           result = read_honeypot_log()
        elif tool_call.function.name == "read_username_log":
           result = read_username_log()
        else: 
           result = "Unknown tool, error"

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result

        })

    second_response = openai_client.chat.completions.create(
    model="gpt-5",
    messages=messages
) 
    print(f"\n{second_response.choices[0].message.content}\n")
else:
    print(f"\n{message.content}\n")
