#general imports
import os
from dotenv import load_dotenv
from typing import Tuple


#langchain imports
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

#other imports
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parser import summary_parser, Summary


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)

    summary_template = """
        given the LinkedIn ifnromation {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
        \n {format_instructions}
    """

    summary_prompt_template = PromptTemplate(input_variables='information', 
                                             template = summary_template, 
                                             partial_variables = {'format_instructions' : summary_parser.get_format_instructions()})

    llm = ChatOpenAI(temperature = 0, model_name= 'gpt-4o-mini')
    #llm = ChatOllama(model = 'gemma3:4b')

    #chain = summary_prompt_template | llm  | StrOutputParser()

    chain = summary_prompt_template | llm | summary_parser

    res:Summary = chain.invoke(input={'information' : linkedin_data})

    return res, linkedin_data.get('photoUrl')



if __name__ == '__main__':

    load_dotenv()
    print('Ice Breaker Enter')
    ice_break_with(name = 'Eden Marco')

    
    
