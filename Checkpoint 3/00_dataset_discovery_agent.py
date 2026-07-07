"""
00_dataset_discovery_agent.py — Phase 0: Ideation & Dataset Discovery

Prompts the user for a high-level sociological hypothesis and uses the Google GenAI SDK
(with offline fallback) to search for and recommend specific, highly-rated datasets (e.g. Zillow, Census) 
required to test the idea.
"""
import os
import sys
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

OFFLINE_RECOMMENDATIONS = {
    "housing": (
        "1. Zillow Research Data (ZHVI/ZORI): ZIP-level monthly index of home values/rents. URL: https://www.zillow.com/research/data/\n"
        "2. Census ACS5 Table B25077 (Median Value) / Table B25064 (Median Gross Rent): ZCTA-level socioeconomic housing indicators."
    ),
    "poverty": (
        "1. Census ACS5 Table S1701 (Poverty Status): ZCTA-level percentage of people below the poverty line.\n"
        "2. USDA Food Access Research Atlas: Track census tract level food deserts and proximity to grocery stores."
    ),
    "health": (
        "1. CDC PLACES Project: Local level health measures (county, ZIP code) for chronic disease and health behaviors.\n"
        "2. Census ACS5 Table S2701 (Health Insurance): Detailed health insurance coverage status by ZCTA."
    ),
    "default": (
        "1. Census ACS5 (American Community Survey 5-Year Estimates): Comprehensive demographic and socioeconomic ZCTA indicators.\n"
        "2. Zillow Home Value Index (ZHVI): ZIP-level property value metrics."
    )
}

def discover_datasets(user_idea: str):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("\n[Resilient Fallback] GEMINI_API_KEY not found in environment. Using offline recommendations.")
        match_fallback(user_idea)
        return
        
    print(f"\n[Agent] Researching datasets for hypothesis: '{user_idea}'...\n")
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Hypothesis: {user_idea}",
            config={
                "system_instruction": (
                    "You are a Data Librarian for sociological and socioeconomic research.\n"
                    "The user will propose a high-level sociological hypothesis.\n"
                    "You must recommend 2-3 specific, real-world datasets/APIs (such as Zillow ZORI/ZHVI, Census ACS5, FDIC, etc.) "
                    "needed to build the modeling frame and test this hypothesis.\n"
                    "Be specific about the table names, variable names, and URLs if possible. Keep your recommendations structured and concise."
                )
            }
        )
        print(response.text)
    except Exception as e:
        print(f"\n[Resilient Fallback] Agent call failed or rate-limited: {e}")
        print("Using offline recommendations.")
        match_fallback(user_idea)

def match_fallback(user_idea: str):
    idea_lower = user_idea.lower()
    found = False
    for key, rec in OFFLINE_RECOMMENDATIONS.items():
        if key in idea_lower and key != "default":
            print(f"Dataset Recommendations for '{key}':")
            print(rec)
            found = True
    if not found:
        print("Dataset Recommendations:")
        print(OFFLINE_RECOMMENDATIONS["default"])

def main():
    print("=== Phase 0: Dataset Discovery Agent ===")
    user_idea = input("Enter your high-level sociological hypothesis (e.g., 'Housing affordability impacts food banks'): ")
    
    if not user_idea.strip():
        print("Idea cannot be empty. Exiting.")
        return
        
    discover_datasets(user_idea)

if __name__ == "__main__":
    main()
