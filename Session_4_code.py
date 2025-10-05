*Main*
Package: WYN-Agent:https://pypi.org/project/wyn-agent/

*Get Started: Install*

! pip install wyn-agent
     
*Get Started: Import*

from google.colab import userdata
MISTRAL_API_KEY = userdata.get('MISTRAL_API_KEY')
     

from wyn_agent.mistral_agent import ChatBot
     
Run Bot

# @title Talk to JARVIS

bot = ChatBot(
    api_key=MISTRAL_API_KEY,
    agent_id="ag:bfb4e4d9:20240809:coding-agent:b1d09feb",
    protocol="You are a code assistant."
)

bot.run_mistral_agent()
     