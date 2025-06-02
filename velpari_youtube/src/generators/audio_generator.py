"""Audio generation module using ElevenLabs.

This module handles the generation of audio files from text using
ElevenLabs' text-to-speech API.
"""

from pathlib import Path
from tqdm import tqdm
from elevenlabs import generate, save, set_api_key
from src.utils.config import Config


class AudioGenerator:
    """Handles audio generation using ElevenLabs.
    
    This class manages the generation and storage of audio files from text
    using ElevenLabs' text-to-speech service.
    
    Args:
        api_key (str): ElevenLabs API key
    """
    
    def __init__(self, api_key: str):
        self.config = Config()
        self.output_dir = Path(self.config.directories['audio'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        set_api_key(api_key)
    
    def generate(self, text: str, index: int) -> Path:
        """Generate audio for a single paragraph.
        
        Args:
            text (str): Text to generate audio for
            index (int): Paragraph index for file naming
        
        Returns:
            Path: Path to the generated audio file
        """
        audio = generate(
            text=text,
            voice=self.config.elevenlabs['default_voice'],
            model=self.config.elevenlabs['model']
        )
        
        audio_path = self.output_dir / f"scene{index}.mp3"
        save(audio, str(audio_path))
        
        return audio_path
    
    def batch_generate(self, paragraphs: list[str]) -> list[Path]:
        """Generate audio for multiple paragraphs.
        
        Args:
            paragraphs (list[str]): List of text paragraphs
        
        Returns:
            list[Path]: List of paths to generated audio files
        """
        print("\n🎙️  Generating audio narration...")
        return [
            self.generate(text, i) 
            for i, text in enumerate(tqdm(
                paragraphs,
                desc="Generating audio",
                unit="paragraph"
            ))
        ] 