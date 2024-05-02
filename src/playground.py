if __name__ != '__main__':
    assert False, 'This module is for testing purposes only'
    
import os
from utilities.image_utils import resize_directory_images
from utilities.video_utils import create_voice_overed_slide, merge_videos
from utilities.audio_utils import text_to_audio
from utilities.web_utils import download_image, search_google_images, search_google_scholar, extract_webpage_contents

if not os.path.exists('temp'):
    os.makedirs('temp')

demo = {
    "serp_mock": True,
    "web_utils": True,
    "audio_utils": False,
    "image_utils": False,
    "video_utils": False,
}

if demo["web_utils"]:
    print("Running search_google_scholar")
    if not demo["serp_mock"]:
        search_results = search_google_scholar("LLMs Multi Agent Collaboration", 3)
    else:
        search_results =[{'title': 'Emergent cooperation and strategy adaptation in multi-agent systems: An extended coevolutionary theory with llms', 'snippet': '… The dynamics and evolution of the Multi-Agent System over time were also … LLMs to facilitate cooperation, enhance social welfare, and promote resilient strategies in multi-agent …', 'link': 'https://www.mdpi.com/2079-9292/12/12/2722'}, {'title': 'AgentCoord: Visually Exploring Coordination Strategy for LLM-based Multi-Agent Collaboration', 'snippet': '… in LLM-based multi-agent collaboration, suggests that our approach can effectively facilitate … LLM-based multi-agent coordination strategies and has the potential to democratize agent …', 'link': 'https://arxiv.org/abs/2404.11943'}, {'title': 'Emergent Cooperation and Strategy Adaptation in Multi-Agent Systems: An Extended Coevolutionary Theory with LLMs', 'snippet': '… The dynamics and evolution of the Multi-Agent System over time were also … LLMs to facilitate cooperation, enhance social welfare, and promote resilient strategies in multi-agent …', 'link': 'https://repositorio.comillas.edu/xmlui/handle/11531/87980'}]
        

    print("Running extract_webpage_contents")
    content = extract_webpage_contents(search_results[1]['link'])
    print("Extracted Content", content)

    print("Running search_google_images")
    if not demo["serp_mock"]:
        image_search = search_google_images("LLMs Multi Agent Collaboration", 3)
    else:
        image_search = [{'title': 'How AutoGen Transforms LLM Applications ...', 'url': 'https://miro.medium.com/v2/0*WKxjYLzDTlFLBAfU.png'}, {'title': 'LLM-Powered Multi-Agent Frameworks ...', 'url': 'https://miro.medium.com/v2/resize:fit:1400/1*wJZZk5aDoMXjK0g2_3V2yg.png'}, {'title': 'Multi-Agent Collaboration ...', 'url': 'https://miro.medium.com/v2/resize:fit:627/1*gVprOgO0qVi5h6Ynigr_aA.png'}]

    print("Running download_image example 1")
    download_image(image_search[0]['url'], 'temp/imgs/test_image_1.jpg')
    print("Running download_image example 2")
    download_image(image_search[1]['url'], 'temp/imgs/test_image_2.jpg')
    print("Running download_image example 3")
    download_image(image_search[2]['url'], 'temp/imgs/test_image_3.jpg')

if demo["image_utils"]:
    print("Running resize_directory_images")
    resize_directory_images((720, 720), 'temp', 'temp/imgs')

if demo["audio_utils"]:
    print("Running text_to_audio example 1")
    text_to_audio("Hello World, this is a test audio! How do I sound?", "temp/test_audio_1.mp3")
    print("Running text_to_audio example 2")
    text_to_audio("I'm an AI agent that generates voice-overed slide.", "temp/test_audio_2.mp3")
    print("Running text_to_audio example 3")
    text_to_audio("I hope you liked my presentation", "temp/test_audio_3.mp3")

if demo["video_utils"]:
    print("Running create_voice_overed_slide example 1")
    create_voice_overed_slide('temp/imgs/test_image_1.jpg', 'temp/test_audio_1.mp3', 'temp/test_video_1.mp4')
    print("Running create_voice_overed_slide example 2")
    create_voice_overed_slide('temp/imgs/test_image_2.jpg', 'temp/test_audio_2.mp3', 'temp/test_video_2.mp4')
    print("Running create_voice_overed_slide example 3")
    create_voice_overed_slide('temp/imgs/test_image_3.jpg', 'temp/test_audio_3.mp3', 'temp/test_video_3.mp4')

    print("Running merge_videos")
    merge_videos(['temp/test_video_1.mp4', 'temp/test_video_2.mp4', 'temp/test_video_3.mp4'], 'temp/merged_video.mp4')