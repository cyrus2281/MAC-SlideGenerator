# MAC-SlideGenerator

Multi-Agent Collaboration voice-overed Slide Generator demo application

## Architecture

![Architecture](./Architecture.png)

## Getting Started

Create a virtual environment and install the required packages:

```bash 
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Note: on windows, use `env\Scripts\activate` instead of `source env/bin/activate`

Create a `.env` file in the root directory and add the following:

```bash
OPENAI_API_KEY=Your_OpenAI_API_Key
SERP_API_KEY=Your_Serp_API_Key
LANGCHAIN_API_KEY=Your_LangChain_API_Key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT="Multi-agent Collaboration"
```

## Agents Architecture

```
1) Planner
1.1) BrainStrommer (self-refine)
   1.1.1) web searcher 
   1.1.2) Web Content Summerizer
1.2) Slide Maker Planner
1.2.1) Bullet Point maker
1.2.2) Image generator
1.3) Production (control and save)
1.3.1) PowerPoint Maker
1.3.2) Audio Generator
1.3.3) Video Maker
```