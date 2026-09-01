# First Agentic AI
I wanted to understand how AI agents work, instead of using a done framework like LangChain without knowing what it actually does. So I build it from scratch with the OpenAI API.

## What I learned
I got a better understanding of the flow. It's two API calls, the first one asks "do you need a tool to answear this?", and if yes I run the function and send the result back in a second call to get the final answer. 

I also learned that small details matter. I had a typo, I wrote "decription" instead of "description" which meant the model never got a description of the search tool. The code still ran it just didn't work as well and I didn't notice right away. So with this in mind it taught me that the code can fail quietly, without throwing an actual error message like I'm used to.

I also only have one round of tool use, so if the model wants to search twice it can't. That will be the next step.

## Setup
1. Clone the repo and go into the folder
2. Create a virtual environment and install the dependencies from 'requirements.txt'
3. Create a .env file with your own OpenAI API key (OPENAI_API_KEY=)

Run the script and type in a question. If the question needs up to date information the agent will decide on its own to search the web before answering.

## Update
After I built a honeypot in Azure to catch and log real attack traffic (another project, linked [here](https://github.com/wtesfamariam/azure-honeypot-soc)), I let this agent actually use the data.
I exported some of the logs as CSV files and added two more tools. The second tool reads through failed login attempts by IP and checks the geolocation, and the third tool reads through the usernames attackers tried. I can now ask the agent "what usernames were attempted the most" and it picks the right file and gives me an answer based on my description.


