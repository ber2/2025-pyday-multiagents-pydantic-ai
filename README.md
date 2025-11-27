# Building AI Agents with Pydantic AI

This repository contains the main setup and code that we will follow during the workshop during [PyDay Barcelona 2025](https://pybcn.org/events/pyday_bcn/pyday_bcn_2025/).

In order to have a smooth setup, I recommend forking this repository and following the instructions in the Prerequisites section below.

At the core of AI agents there is the need to interact with an LLM, so in the instructions below you will have a choice:

- If you have a powerful device with a GPU, or want a completely _free_ experience, you may run your own LLM via Ollama. We recommend Llama 3.1 & 3.2, with 3b and 8b sizes.
- Otherwise, it is possible to obtain a _generous free tier_ on the Google Gemini API, especially when using the Gemini Flash models, which is sufficient for this workshop.

Optionally, we will use the [Logfire](https://logfire-eu.pydantic.dev/) platform in order to showcase what happens when a call to a Pydantic agent is done. This platform also has a very _generous free tier_ which is sufficient for the purpose of this project.

The workshop is presented as a series of exercises following a [TDD red-green-refactor](https://en.wikipedia.org/wiki/Test-driven_development) pattern. At each stage, you will checkout a new branch having a set of failing unit tests, mostly due to missing code implementations. By implementing the missing code and making the tests pass, you will be able to make progress. Solutions are available on separate branches, so you can check your own work.

The main branch is the starting point. It already contains some useful code for the workshop. There is a script that, given an arXiv id, will download the PDF for the corresponding paper and extract its text. It may be called as follows:
```bash
uv run arxiv-parser "1706.03762v7"
```

As we progress through the workshop, we will enrich this script in order to obtain structured information about paper authors and their affiliations.


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

### 2. Choose Your LLM

You need to set up at least one of these options:

#### Option A: Ollama (Local, Free)

1. Install Ollama from [ollama.ai](https://ollama.ai)

2. Download a model (we recommend llama3.2 or llama3.1, updated list of models [here](https://ollama.com/search)):
```bash
ollama pull llama3.2:3b
```

#### Option B: Google Gemini (API, Requires Key)

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey) (a google account is required for logging in)

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
# LLM Configuration
# Choose one or both options:

# Option A: Google Gemini (API, requires key)
MODEL_NAME=gemini-2.5-flash
GEMINI_API_KEY=your-api-key-here

# Option B: Ollama (local, free)
MODEL_NAME=ollama:llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434/v1

# Observability (optional but recommended)
# Sign up at: https://logfire.pydantic.dev
LOGFIRE_TOKEN=your-logfire-token-here
```

### 6. Verify Setup

At this stage, you should be able to run the unit tests by calling:

```bash
uv run pytest
```

Provided that dependencies are installed, you should see about 20 tests passing, and you'll be ready to start the workshop.

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
