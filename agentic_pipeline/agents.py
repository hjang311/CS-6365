import os
from google.antigravity import Agent, LocalAgentConfig

def get_config():
    """Retrieve the Gemini API key and configure the agent."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY is not set. Please add it to your .env file.")
    return LocalAgentConfig(api_key=api_key)

def get_prompt_from_file(relative_path):
    """Utility function to read the SKILL.md file from the .agent/skills directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", relative_path)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def create_orchestrator():
    """Creates the Orchestrator Agent responsible for high-level strategy."""
    orchestrator_prompt = get_prompt_from_file(os.path.join(".agent", "skills", "norp-orchestrator", "SKILL.md"))
    return Agent(
        config=get_config(),
        system_instruction=orchestrator_prompt
    )

def create_code_agent():
    """Creates the Code Agent responsible for Python REPL execution."""
    code_agent_prompt = get_prompt_from_file(os.path.join(".agent", "skills", "norp-code-agent", "SKILL.md"))
    return Agent(
        config=get_config(),
        system_instruction=code_agent_prompt
    )

def create_validator_agent():
    """Creates the Validator Agent responsible for Programmatic Verification."""
    validator_prompt = get_prompt_from_file(os.path.join(".agent", "skills", "norp-validator-agent", "SKILL.md"))
    return Agent(
        config=get_config(),
        system_instruction=validator_prompt
    )
