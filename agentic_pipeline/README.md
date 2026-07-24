# Agentic Data Exploration Pipeline (legacy SDK scaffolding)

> **Phase 3 (rolled loop) lives in [`Checkpoint 4/`](../Checkpoint%204/).**  
> This folder retains early Antigravity SDK factories (`agents.py`, hybrid prompts).
> Prefer `.agent/skills/norp-*` + `Checkpoint 4/09_phase3_agentic_loop.py` for the
> educational curriculum. See [`docs/CURRICULUM.md`](../docs/CURRICULUM.md).

---

# Agentic Data Exploration Pipeline (CS 6365)

This repository contains the Phase 1 implementation of the Agentic Data Exploration Layer. 

## Overview
The goal of this pipeline is to use the `google-antigravity` SDK to autonomously profile, clean, and discover sociological correlations in non-profit dataset environments. 

## Current Implementation (Phase 1: Foundation & Triage Gate)
- **`ingest_and_profile.py`**: A foundational script to profile the provided Form 990 CSV data using `pandas` and the `pyarrow` engine.
- **`agents.py`**: Defines the `Orchestrator Agent` and `Code Agent` system prompts and configuration using the `google-antigravity` SDK.
- **`main.py`**: The entry point to initialize the environment and run the pipeline.

## Setup Instructions

> [!IMPORTANT]
> **Windows Users:** The `google-antigravity` SDK requires pre-compiled binaries that are currently only available for Linux and Apple Silicon (Mac). It cannot be installed natively on Windows. You **must** use Windows Subsystem for Linux (WSL) or Docker.

### Windows Setup (via WSL)
If you are on Windows, follow these steps to set up a Linux environment:
1. Open PowerShell as Administrator and install WSL (with Ubuntu):
   `wsl --install`
2. Restart your computer if prompted, and open the Ubuntu app to create your username/password.
3. In the Ubuntu terminal, ensure Python 3.10+ and pip/venv are installed:
   `sudo apt update && sudo apt install python3 python3-pip python3-venv -y`
4. Navigate to your Windows project directory from within WSL:
   `cd /mnt/c/Users/YOUR_USERNAME/path/to/CS-6365/agentic_pipeline`
5. Proceed to the standard project setup below.

### Standard Project Setup (Linux, Mac, or WSL)
1. Ensure you have Python 3.10 or higher.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Upgrade pip and install dependencies:
   ```bash
   pip install --upgrade pip
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
