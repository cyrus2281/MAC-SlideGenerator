# MAC-SlideGenerator

Multi-Agent Collaboration: Voice-overed video slide generator

## Architecture

![Architecture](./architecture.png)

## Getting Started

Install Docker on your machine.

### From Docker Hub

1. Pull the Docker image from Docker Hub

```bash
docker pull cyrus2281/mac-slider-generator:latest
```

2. Create a `.env` file in the root directory and add the following:

```bash
OPENAI_API_KEY=Your_OpenAI_API_Key
SERP_API_KEY=Your_Serp_API_Key
LANGCHAIN_API_KEY=Your_LangChain_API_Key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT="Multi-agent Collaboration"
```

3. Create a `projects` directory in your working directory.

```bash
mkdir projects
```


4. Run the docker run command to start the container

Update the `.env` path if it is not in the root directory.

Update `${PWD}/projects` to the path of the `projects` directory if it is not in the working directory.

```bash
docker run --rm --env-file .env -it -v ${PWD}/projects:/app/projects cyrus2281/mac-slider-generator:latest
```

### Building the Docker Image Yourself

1. Navigate to the root directory of the project and run the following command to build the Docker image

```bash 
docker build -t mac-slider-generator .
```

2. Create a `.env` file in the root directory and add the following:

```bash
OPENAI_API_KEY=Your_OpenAI_API_Key
SERP_API_KEY=Your_Serp_API_Key
LANGCHAIN_API_KEY=Your_LangChain_API_Key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT="Multi-agent Collaboration"
```

3. Run the docker run command to start the container

```bash
docker run --rm --env-file .env -it -v ${PWD}:/app mac-slider-generator
```

## Customization

Further environment variables can be added to the `.env` file to customize the behavior of the app.

```bash
OPENAI_GPT_MODEL_NAME=Your_OpenAI_GPT_Model_Name
USE_OPENAI_FOR_TEXT_TO_AUDIO=Wether_to_use_OpenAI_for_text_to_audio
SLIDES_WATERMARK=Your_Slides_Watermark
EXTENDED_SLIDES=false
```

- `OPENAI_GPT_MODEL_NAME`: The OpenAI GPT model to use for generating text. Default is `gpt-4o`.
- `USE_OPENAI_FOR_TEXT_TO_AUDIO`: Whether to use OpenAI for text to audio conversion. Default is `true`.
- `SLIDES_WATERMARK`: The watermark to add to the slides. Default is `MAC-Slide-Generator by Cyrus Mobini`.
- `EXTENDED_SLIDES`: Whether to generate more slides (10~15 slides). Default is `false` (around 6~9 slides). This will increase the cost of the service.