"""
00_dataset_discovery_agent.py — Phase 0: Ideation & Dataset Discovery

Prompts the user for a high-level sociological hypothesis and uses the Antigravity Agent
interactive prompt to search for and recommend specific datasets.
"""
import os
import sys

def discover_datasets(user_idea: str):
    print(f"\n[Agent] Researching datasets for hypothesis: '{user_idea}'...\n")
    
    # Prompt the Antigravity Agent to generate the response
    print("====================================================================")
    print("AGENT ACTION REQUIRED: Please act as the Data Librarian LLM.")
    print("System Instruction: You are a Data Librarian for sociological and socioeconomic research.")
    print("The user will propose a high-level sociological hypothesis.")
    print("You must recommend 2-3 specific, real-world datasets/APIs (such as Zillow ZORI/ZHVI, Census ACS5, FDIC, etc.) needed to build the modeling frame and test this hypothesis.")
    print("Be specific about the table names, variable names, and URLs if possible. Keep your recommendations structured and concise.")
    print(f"User Idea: {user_idea}")
    print("---")
    print("Please paste the generated dataset recommendations below. Type 'END_OF_RESPONSE' on a new line when finished.")
    print("====================================================================")
    
    response_lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END_OF_RESPONSE":
                break
            response_lines.append(line)
        except EOFError:
            break
            
    response_text = "\n".join(response_lines)
    print("\n=== Dataset Recommendations ===")
    print(response_text)

def main():
    print("=== Phase 0: Dataset Discovery Agent ===")
    user_idea = input("Enter your high-level sociological hypothesis (e.g., 'Housing affordability impacts food banks'): ")
    
    if not user_idea.strip():
        print("Idea cannot be empty. Exiting.")
        return
        
    discover_datasets(user_idea)

if __name__ == "__main__":
    main()
