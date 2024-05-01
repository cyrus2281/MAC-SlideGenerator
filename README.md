# MAC-SlideGenerator

Multi-Agent Collaboration voice-overed Slide Generator demo application

## Getting Started

Create a virtual environment and install the required packages:

```bash 
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Note: on windows, use `env\Scripts\activate` instead of `source env/bin/activate`

## Agents Architecture

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
