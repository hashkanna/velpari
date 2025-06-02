"""Media combination utility.

This module provides functionality to combine existing audio and image files
into videos, with support for both single and batch processing.
"""

from pathlib import Path
from typing import List, Tuple
import re
from tqdm import tqdm
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from src.utils.config import Config


class MediaCombiner:
    """Combines audio and image files into videos.
    
    This class provides utilities to:
    1. Combine a single audio-image pair into a video
    2. Process multiple pairs and combine them into one video
    3. Sort files naturally (e.g., part1 before part10)
    """
    
    def __init__(self, input_dir: str = None, output_dir: str = None):
        """Initialize the combiner with input/output directories.
        
        Args:
            input_dir (str, optional): Directory containing media files
            output_dir (str, optional): Directory for output videos
        """
        self.config = Config()
        self.input_dir = Path(input_dir) if input_dir else Path("input/media")
        
        # Handle output directory
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path(self.config.directories["output"])
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def natural_sort_key(s: str) -> List[Tuple[str, int]]:
        """Key for natural sorting of strings with numbers.
        
        Args:
            s (str): String to convert to sort key
        
        Returns:
            List[Tuple[str, int]]: Sort key that handles numbers properly
        """
        return [(str, int(num)) if num else (txt, 0)
                for txt, num in re.findall(r'([^0-9]*)([0-9]*)', s)]
    
    def find_matching_files(self) -> List[Tuple[Path, Path]]:
        """Find matching audio and image files in input directory.
        
        Returns:
            List[Tuple[Path, Path]]: List of (audio_path, image_path) pairs
        """
        # Get all mp3 and image files
        audio_files = sorted(
            [f for f in self.input_dir.glob("*.mp3")],
            key=lambda x: self.natural_sort_key(x.stem)
        )
        image_files = sorted(
            [f for f in self.input_dir.glob("*.jpg")],
            key=lambda x: self.natural_sort_key(x.stem)
        )
        
        # Match files by their base names
        pairs = []
        for audio in audio_files:
            matching_image = next(
                (img for img in image_files if img.stem == audio.stem),
                None
            )
            if matching_image:
                pairs.append((audio, matching_image))
            else:
                print(f"⚠️  Warning: No matching image for {audio.name}")
        
        return pairs
    
    def create_clip(self, audio_path: Path, image_path: Path) -> ImageClip:
        """Create a video clip from an audio-image pair.
        
        Args:
            audio_path (Path): Path to audio file
            image_path (Path): Path to image file
        
        Returns:
            ImageClip: Video clip with synchronized audio
        """
        audio = AudioFileClip(str(audio_path))
        image = ImageClip(str(image_path))
        video = image.set_duration(audio.duration)
        return video.set_audio(audio)
    
    def combine_all(self, output_name: str = None) -> Path:
        """Combine all matching media files into a single video.
        
        Args:
            output_name (str, optional): Name for output video file
        
        Returns:
            Path: Path to the generated video file
        """
        print("\n🔍 Finding matching media files...")
        pairs = self.find_matching_files()
        
        if not pairs:
            raise ValueError("No matching audio-image pairs found")
        
        print(f"\n📂 Found {len(pairs)} matching pairs")
        
        print("\n🎬 Creating video clips...")
        clips = [
            self.create_clip(audio, image)
            for audio, image in tqdm(pairs, desc="Creating clips", unit="clip")
        ]
        
        print("\n🎥 Combining clips into final video...")
        final_video = concatenate_videoclips(clips)
        
        # Handle output path
        if output_name:
            # If output_name is a full path, use it directly
            if '/' in output_name:
                output_path = Path(output_name)
                output_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                # Otherwise, put it in the output directory
                output_path = self.output_dir / output_name
        else:
            output_path = self.output_dir / "combined_video.mp4"
        
        print("\n💾 Encoding final video...")
        final_video.write_videofile(
            str(output_path),
            fps=self.config.video["fps"],
            codec=self.config.video["video_codec"],
            preset=self.config.video["video_preset"],
            audio_codec="aac",  # Use AAC for YouTube compatibility
            audio_bitrate="320k",  # High quality audio
            ffmpeg_params=[
                "-crf", str(self.config.video["video_quality"]),
                "-pix_fmt", self.config.video["pixel_format"]
            ]
        )
        
        return output_path 