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
    """Creates the Code Agent (Phase 3 Stats Engine operator)."""
    code_agent_prompt = get_prompt_from_file(os.path.join(".agent", "skills", "norp-code-agent", "SKILL.md"))
    return Agent(
        config=get_config(),
        system_instruction=code_agent_prompt
    )

def create_validator_agent():
    """Creates the Critic / Validator Agent."""
    validator_prompt = get_prompt_from_file(os.path.join(".agent", "skills", "norp-validator-agent", "SKILL.md"))
    return Agent(
        config=get_config(),
        system_instruction=validator_prompt
    )

def create_scout_agent():
    """Creates the Scout Agent (source discovery / routing)."""
    prompt = get_prompt_from_file(os.path.join(".agent", "skills", "norp-scout", "SKILL.md"))
    return Agent(config=get_config(), system_instruction=prompt)

def create_acquisition_agent():
    """Creates the Acquisition Agent (named adapters only)."""
    prompt = get_prompt_from_file(os.path.join(".agent", "skills", "norp-acquisition", "SKILL.md"))
    return Agent(config=get_config(), system_instruction=prompt)

def create_researcher_agent():
    """Creates the Researcher Agent (propose + interpret; never OLS)."""
    prompt = get_prompt_from_file(os.path.join(".agent", "skills", "norp-researcher", "SKILL.md"))
    return Agent(config=get_config(), system_instruction=prompt)

def create_phase3_agents():
    """Return the five Phase 3 cognitive agents (Stats Engine remains the 09 CLI)."""
    return {
        "orchestrator": create_orchestrator(),
        "scout": create_scout_agent(),
        "acquisition": create_acquisition_agent(),
        "researcher": create_researcher_agent(),
        "critic": create_validator_agent(),
        "code": create_code_agent(),
    }
