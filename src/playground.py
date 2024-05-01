if __name__ != '__main__':
    assert False, 'This module is for testing purposes only'
    
from utilities.image_utils import resize_directory_images
from utilities.video_utils import create_voice_overed_slide, merge_videos
from utilities.audio_utils import text_to_audio
import os

if not os.path.exists('temp'):
    os.makedirs('temp')

print("Running resize_directory_images")
resize_directory_images((720, 720), 'temp', 'temp/imgs')

print("Running text_to_audio example 1")
text_to_audio("Hello World, this is a test audio! How do I sound?", "temp/test_audio_1.mp3")
print("Running text_to_audio example 2")
text_to_audio("I'm an AI agent that generates voice-overed slide.", "temp/test_audio_2.mp3")
print("Running text_to_audio example 3")
text_to_audio("I hope you liked my presentation", "temp/test_audio_3.mp3")

print("Running create_voice_overed_slide example 1")
create_voice_overed_slide('temp/imgs/test_image_1.jpg', 'temp/test_audio_1.mp3', 'temp/test_video_1.mp4')
print("Running create_voice_overed_slide example 2")
create_voice_overed_slide('temp/imgs/test_image_2.jpg', 'temp/test_audio_2.mp3', 'temp/test_video_2.mp4')
print("Running create_voice_overed_slide example 3")
create_voice_overed_slide('temp/imgs/test_image_3.jpg', 'temp/test_audio_3.mp3', 'temp/test_video_3.mp4')

print("Running merge_videos")
merge_videos(['temp/test_video_1.mp4', 'temp/test_video_2.mp4', 'temp/test_video_3.mp4'], 'temp/merged_video.mp4')