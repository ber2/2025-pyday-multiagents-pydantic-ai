# Building AI Agents with Pydantic AI

Workshop materials for PyBcn PyDay 2025 - Multi-agent systems using Pydantic AI to parse arXiv papers.

## Prerequisites

### 0. Fork This Repository

**IMPORTANT:** Before starting, fork this repository to your own GitHub account. This allows you to:
- Save your work and progress
- Make commits without affecting the original repository
- Continue working on the project after the workshop

1. Click the "Fork" button at the top right of this repository
2. Clone **your fork** (not the original repository):

```bash
git clone https://github.com/YOUR-USERNAME/2025-pyday-multiagents-pydantic-ai.git
cd 2025-pyday-multiagents-pydantic-ai
```

### 1. Install uv

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv
```

### 2. Choose Your LLM Option

You need to set up at least one of these options:

#### Option A: Ollama (Local, Free)

1. Install Ollama from [ollama.ai](https://ollama.ai)

2. Download a model (we recommend llama3.2 or llama3.1):
```bash
ollama pull llama3.2
```

3. Verify it's running:
```bash
ollama list
```

#### Option B: Google Gemini (API, Requires Key)

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

2. Save it for the .env file setup below

### 3. Set Up Logfire (Optional but Recommended)

Logfire provides observability for your AI agents.

1. Sign up at [logfire.pydantic.dev](https://logfire.pydantic.dev)
2. Create a new project
3. Get your write token from the project settings

### 4. Install Python Dependencies

```bash
# From the repository root directory
uv sync
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your tokens:

```bash
# Choose one or both LLM options:

# Option A: Ollama (local)
OLLAMA_MODEL=llama3.2

# Option B: Gemini (API)
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Logfire (for observability)
LOGFIRE_TOKEN=your_logfire_token_here
```

### 6. Verify Setup

Run the setup verification script:

```bash
uv run python verify_setup.py
```

This will check:
- Python dependencies are installed
- At least one LLM option is configured and working
- Logfire connection (if configured)

## Git Branch Workflow

The workshop uses different git branches for smooth transitions between parts:

- **`main`**: Current branch - setup and utilities
- **`part1-scaffold`**: Start of Part 1 - checkout here when Part 1 begins
- **`part1-solution`**: Complete Part 1 code - reference if you get stuck
- **`part2-scaffold`**: Start of Part 2 - checkout here when Part 2 begins (includes Part 1 solution)
- **`part2-solution`**: Complete implementation - final demo

During the workshop, you'll switch branches as instructed. Don't worry about losing your work - you can always commit your changes before switching or stash them with `git stash`.

## Quick Start

Once setup is complete, you can test the complete solution:

```bash
# Checkout the complete solution
git checkout part2-solution

# Run the CLI tool
uv run python -m arxiv_parser "1706.03762v7"
```

This will download an arXiv paper and extract structured author/affiliation data.
