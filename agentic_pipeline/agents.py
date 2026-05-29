import os
from google.antigravity import Agent, LocalAgentConfig

def get_config():
    """Retrieve the Gemini API key and configure the agent."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY is not set. Please add it to your .env file.")
    return LocalAgentConfig(api_key=api_key)

def create_orchestrator():
    """Creates the Orchestrator Agent responsible for high-level strategy."""
    orchestrator_prompt = """
    You are the Orchestrator Agent for the CS 6365 Non-Profit Data Exploration Project.
    Your job is to receive a sociological hypothesis, profile the available datasets,
    and delegate specific Python coding tasks to the Code Agent.
    """
    return Agent(
        config=get_config(),
        system_instruction=orchestrator_prompt
    )

def create_code_agent():
    """Creates the Code Agent responsible for Python REPL execution."""
    code_agent_prompt = """
    You are the Code Agent. You execute data cleaning, merging, and statistical modeling
    tasks using Python (pandas, scikit-learn).
    You operate inside a REPL sandbox. If your code fails, you must read the traceback
    and correct your script.
    """
    return Agent(
        config=get_config(),
        system_instruction=code_agent_prompt
    )
