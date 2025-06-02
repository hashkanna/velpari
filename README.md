# Velpari Project

A comprehensive collection and processing system for Velpari, a Tamil historical novel series. This repository contains digitized versions of the original Vikatan magazine publications, along with tools for processing and managing the content.

## Content Overview

### PDF Collection
The `velpari_pdf` directory contains high-quality scans of the original Velpari series from Vikatan magazine, spanning multiple issues. These PDFs preserve the original Tamil text, illustrations, and layout from the magazine publications.

### YouTube Content
The `velpari_youtube` module contains tools for processing and managing YouTube content related to Velpari, including:
- Audio narrations
- Video adaptations
- Educational content
- Fan discussions and analyses

## Historical Significance

Velpari is a significant work in Tamil literature that:
- Chronicles the life and times of the legendary Vel Pari, a king of the Parambu Nadu
- Provides insights into ancient Tamil culture, warfare, and governance
- Features rich character development and historical accuracy
- Has influenced numerous adaptations across different media

## Content Organization

```
.
├── velpari_pdf/         # Original magazine scans (issues 1-111)
├── velpari_youtube/     # YouTube content processing tools
└── [other files]       # Additional resources including:
    ├── Audio narrations
    ├── Full text versions
    └── Supplementary materials
```

## Technical Details

The repository includes tools for:
- PDF text extraction and processing
- YouTube content management
- Audio processing and synchronization
- Content indexing and search

### Technologies Used

#### AI & ML Tools
- **OpenAI GPT-4**: Used for advanced text processing, content summarization, and generating contextual descriptions
- **ElevenLabs**: Powers high-quality Tamil text-to-speech conversion for audio narrations
- **Whisper**: Handles speech-to-text conversion for video content and audio processing

#### Content Processing
- **PyPDF2**: PDF text extraction and manipulation
- **FFmpeg**: Audio/video processing and format conversion
- **yt-dlp**: YouTube content downloading and processing

#### Development Tools
- **Python**: Core programming language
- **FastAPI**: Backend API development
- **SQLite**: Local content indexing and search

[Setup and usage instructions moved to CONTRIBUTING.md]

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for setup and contribution guidelines. 