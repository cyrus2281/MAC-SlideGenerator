# MAC-SlideGenerator

Multi-Agent Collaboration: Voice-overed video slide generator - Demo application

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
