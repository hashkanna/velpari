"""Image generation module using OpenAI's DALL-E.

This module handles the generation of images for text paragraphs using
OpenAI's DALL-E API, with support for regenerating specific images.
"""

from pathlib import Path
import requests
from tqdm import tqdm
from openai import OpenAI
from src.utils.config import Config
from src.utils.story_processor import StoryProcessor


class ImageGenerator:
    """Handles image generation using DALL-E.
    
    This class manages the generation and storage of images for text
    paragraphs using OpenAI's DALL-E image generation service.
    
    Args:
        api_key (str): OpenAI API key
    """
    
    def __init__(self, api_key: str):
        self.config = Config()
        self.output_dir = Path(self.config.directories['images'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.client = OpenAI(api_key=api_key)
        self.story_processor = StoryProcessor()
        self.current_chapter = None  # Will be set by set_chapter()
    
    def set_chapter(self, chapter_number: int):
        """Set the current chapter number for base prompt selection.
        
        Args:
            chapter_number (int): Chapter number
        """
        self.current_chapter = chapter_number
    
    def get_base_prompt(self) -> str:
        """Get the base prompt for the current chapter.
        
        Returns:
            str: Base prompt for image generation
            
        Raises:
            FileNotFoundError: If base prompt file doesn't exist
            ValueError: If chapter number not set
        """
        if self.current_chapter is None:
            msg = "Chapter number not set. Call set_chapter() first."
            raise ValueError(msg)
            
        # Get the path that will be checked
        path = self.story_processor.get_base_prompt_path(self.current_chapter)
        print(f"\nLooking for base prompt at: {path}")
        
        file_prompt = self.story_processor.read_base_prompt(
            self.current_chapter
        )
        if not file_prompt:
            chapter = self.current_chapter
            raise FileNotFoundError(
                f"Base prompt file not found for chapter {chapter}"
            )
            
        print(f"Found base prompt ({len(file_prompt)} chars):")
        print("---")
        print(file_prompt)
        print("---")
        
        return file_prompt
    
    def generate(self, text: str, index: int) -> Path:
        """Generate image for a single paragraph.
        
        Args:
            text (str): Text to generate image for
            index (int): Paragraph index for file naming
        
        Returns:
            Path: Path to the generated image file
        """
        base_prompt = self.get_base_prompt()
        prompt = f"{base_prompt} Context: {text}"
        
        print(f"\nPrompt for image {index}:")
        print("---")
        print(prompt)
        print("---")
        
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        image_path = self.output_dir / f"image_{index}.png"
        
        response = requests.get(image_url)
        with open(image_path, "wb") as f:
            f.write(response.content)
        
        return image_path
    
    def batch_generate(self, paragraphs: list[str]) -> list[Path]:
        """Generate images for multiple paragraphs.
        
        Args:
            paragraphs (list[str]): List of text paragraphs
        
        Returns:
            list[Path]: List of paths to generated image files
        """
        print("\n🎨 Generating visuals...")
        return [
            self.generate(text, i)
            for i, text in enumerate(tqdm(
                paragraphs,
                desc="Generating images",
                unit="image"
            ))
        ]
    
    def regenerate(self, text: str, index: int) -> Path:
        """Regenerate image for a specific paragraph.
        
        Args:
            text (str): Text to generate image for
            index (int): Paragraph index for file naming
        
        Returns:
            Path: Path to the regenerated image file
        """
        print("\n🎨 Regenerating image...")
        return self.generate(text, index) 