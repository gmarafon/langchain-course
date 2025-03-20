#general imports
import sys
import os
from dotenv import load_dotenv
load_dotenv()

#pythonpath
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#langchain imports
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

#packages
from tools.tools import get_profile_url_tavily

def lookup(name: str) -> str:

    llm = ChatOpenAI(temperature=0, model_name = 'gpt-4o-mini')

    #llm = ChatOllama(model = 'gemma3:4b')

    template = '''
        Given the full name {person_name} I want you to get it me a link to their LinkedIn profile page. 
        Your answer should contain only a URL
        '''

    prompt_template = PromptTemplate(template = template, input_variables=['person_name'])

    tools_for_agent = [
        Tool (
            name = 'Crawl Google for Linkedin profile page',
            func = get_profile_url_tavily,
            description = 'useful for when you need to get the Linkedin page URL'
        )
    ]

    react_prompt = hub.pull('hwchase17/react')
    agent = create_react_agent(llm = llm, tools= tools_for_agent, prompt = react_prompt)
    agent_executor = AgentExecutor(agent= agent, tools = tools_for_agent, verbose = True)

    result = agent_executor.invoke(
        input = {'input' : prompt_template.format_prompt(person_name = name)}
    )

    linkedin_profile_url = result['output']
    return linkedin_profile_url


if __name__ == '__main__':
    linkedin_url = lookup(name = 'Eden Marco')
    print(linkedin_url)