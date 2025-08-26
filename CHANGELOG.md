# Changelog

All notable changes to Thunderbolts will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-08-07

### Added
- **Core Features**
  - Multi-format content processing (video, audio, documents)
  - Advanced memory system with short-term and long-term memory
  - Intelligent text analysis and summarization
  - Semantic search with vector database
  - Web fallback search capabilities
  - Streamlit web interface

- **AI Integration**
  - Azure OpenAI and OpenAI API support
  - LangChain integration for advanced AI workflows
  - Sentence transformers for embeddings
  - Multi-modal AI capabilities (when API configured)

- **Text Processing**
  - Advanced text cleaning and preprocessing
  - Intelligent chunking algorithms
  - Grammar checking with LanguageTool (Java 17+ required)
  - Multi-language support

- **Audio Processing**
  - Speech-to-text conversion
  - Audio enhancement and noise reduction
  - Vocal separation capabilities
  - Multiple audio format support

- **Database & Search**
  - FAISS vector database integration
  - ChromaDB support
  - Semantic search with reranking
  - Multi-hop retrieval system

- **Memory System**
  - Conversation tracking and context management
  - Automatic memory consolidation
  - Configurable memory retention policies
  - Performance metrics tracking

### Technical Improvements
- **Dependency Management**
  - Graceful fallbacks for missing dependencies
  - NumPy 1.x compatibility maintained
  - Comprehensive error handling
  - Modular architecture with optional components

- **Performance**
  - Efficient caching system
  - Optimized vector operations
  - Batch processing capabilities
  - Memory usage optimization

- **Developer Experience**
  - Comprehensive logging system
  - Detailed error messages
  - Extensive documentation
  - Test coverage for core components

### System Requirements
- Python 3.9+
- Conda environment support
- Optional: FFmpeg for video processing

### Known Issues
- MoviePy disabled due to dependency conflicts (video processing limited)
- Some dependency conflicts with thinc/spaCy (non-critical)
- Requires manual Java setup for grammar checking

### Dependencies
- streamlit>=1.28.0
- langchain>=0.3.0
- sentence-transformers>=2.2.2
- numpy>=1.24.0,<2.0.0 (compatibility constraint)
- chromadb>=1.0.0
- faiss-cpu>=1.7.4
- And many more (see requirements.txt)

## [Unreleased]

### Planned Features
- Enhanced video processing capabilities
- Advanced multi-modal AI features
- Real-time collaboration features
- API endpoint for programmatic access
- Mobile-responsive interface improvements

### Changes
- i18n: Localized all Streamlit UI (Notebooks, Settings), added Import/Export section translations
- Settings: Removed show_processing_time, show_confidence_score, enable_animations; removed local theme selector; reordered tabs (Interface, Model, Search, Audio, Memory, Advanced)
- YouTube: Updated yt-dlp options to reduce 403/format errors; prioritized audio-only formats; switched to OpenAI Whisper API; included video description in chunks
- Sorting: Use stable internal keys for notebook sorting independent of translated labels

---

For more details about each release, see the [GitHub releases page](https://github.com/Thunderbolts/Thunderbolts/releases).
