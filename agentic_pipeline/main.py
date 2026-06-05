import asyncio
from dotenv import load_dotenv
from agents import create_orchestrator, create_code_agent

async def main():
    # Load environment variables from .env file
    load_dotenv()
    
    print("Initializing Agentic Data Exploration Layer...")
    
    # Instantiate the agents
    orchestrator = create_orchestrator()
    code_agent = create_code_agent()
    
    # Phase 1: Simulate the Triage Gate task
    initial_task = "We have an 88MB CSV file named 'query_result_2026-05-29T15_00_45.06955553-04_00.csv'. Please outline how the Code Agent should execute the Phase 1 Triage Gate profiling on this dataset."
    
    print(f"\n[Orchestrator Task]: {initial_task}")
    
    # Interact with the Orchestrator Agent
    async with orchestrator as agent:
        response = await agent.chat(initial_task)
        print("\n[Orchestrator Response]:")
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())
