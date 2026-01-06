
# Asana Workspace Simulation

A Python tool to generate realistic seed data mimicking a large B2B SaaS organization's Asana workspace (Users, Teams, Projects, Tasks, Comments).

## Features
- **Realistic Data**: Uses `Faker` for users and industry templates for projects/tasks.
- **LLM Integration**: Optionally uses Google Gemini to generate rich text descriptions and comments.
- **Scalable**: Can generate 5000+ users and associated data.
- **Schema Compliance**: Fully relational SQLite database mirroring Asana's core entities.

## How to get the API Key
Below are the steps to generate the gemini api key that is to be used in this repo.

- Sign in to https://aistudio.google.com/ 
- Bottom left near the profile logo, there will be an option Get API Key , select it.
- Click Create API Key, if there is no project available, create a new one by following the details.
- Enter a name and select a project from dropdown.
- You would be able to see your API Key and its details in the console.


## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup**
   To enable LLM generation , set your API key. (Without API Key the code will use default scraped dummy values)
   ```bash
   # Windows PowerShell
   $env:GEMINI_API_KEY="your-key-here"
   ```

## Usage

### Run Simulation
```bash
python src/main.py
```


The output database will be created at `output/asana_simulation.sqlite`.

## Project Structure
- `schema.sql`: Database definition.
- `src/generators/`: logic for creating Users, Teams, Projects, etc.
- `src/main.py`: Orchestrator script.
- `src/scrapers/`: Scripts to fetch/generate seed data (YC companies, Census names, etc). 
- `DOCUMENTATION.md`: Detailed methodology and schema design.

## Data Regeneration
To update the seed data sources (CSVs in `src/scrapers/data/`):
```bash
python src/scrapers/run_scrapers.py
```
