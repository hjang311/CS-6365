# Agentic Data Exploration Pipeline (CS 6365)

This repository contains the Phase 1 implementation of the Agentic Data Exploration Layer. 

## Overview
The goal of this pipeline is to use the `google-antigravity` SDK to autonomously profile, clean, and discover sociological correlations in non-profit dataset environments. 

## Current Implementation (Phase 1: Foundation & Triage Gate)
- **`ingest_and_profile.py`**: A foundational script to profile the provided Form 990 CSV data using `pandas` and the `pyarrow` engine.
- **`agents.py`**: Defines the `Orchestrator Agent` and `Code Agent` system prompts and configuration using the `google-antigravity` SDK.
- **`main.py`**: The entry point to initialize the environment and run the pipeline.

## Setup Instructions
1. Install Python 3.10 or higher.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example` and add your API Key:
   ```
   GEMINI_API_KEY="your_api_key_here"
   ```
5. Run the Phase 1 Orchestrator:
   ```bash
   python main.py
   ```
