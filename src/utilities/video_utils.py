import os
from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips, concatenate_audioclips

blank_audio_path =  os.path.join("src", "assets", "500-milliseconds-of-silence.mp3")
blank_audio_clip = AudioFileClip(blank_audio_path)

def create_voice_overed_slide(input_image, input_audio, output_file):
    # Load the image clip
    image_clip = ImageClip(input_image)
    # Load the audio clip
    audio_clip = AudioFileClip(input_audio)
    # Create a padded audio by concatenating the audio clip with blank padding
    padded_audio = concatenate_audioclips([audio_clip, blank_audio_clip])
    # Set the duration of the image clip to match the audio clip
    image_clip = image_clip.set_duration(padded_audio.duration)
    # Set the audio of the image clip to the loaded audio clip + blank padding
    image_clip = image_clip.set_audio(padded_audio)
    # Write the final video file
    image_clip.write_videofile(output_file, fps=12, logger=None)
    
    audio_clip.close()
    image_clip.close()

def merge_videos(videos_list, output_video):
    # Create an empty list to store the video clips
    video_clips = []
    # Iterate over each video path in the videos_list
    for video_path in videos_list:
        # Load the video clip
        video_clip = VideoFileClip(video_path)
        # Append the video clip to the list
        video_clips.append(video_clip)
    
    # Concatenate the video clips into a single video
    final_clip = concatenate_videoclips(video_clips)
    
    # Write the final video file
    final_clip.write_videofile(output_video, fps=12, logger=None)

    # Closing resources
    for video_path in videos_list:
        video_clip.close()
    final_clip.close()

    
