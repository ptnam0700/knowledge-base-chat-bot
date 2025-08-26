"""
Simple YouTube processing module for Thunderbolts.
Handles YouTube video info extraction, transcript generation, and content enrichment.
"""
import os
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, Union, List
from urllib.parse import urlparse, parse_qs
from src.utils.logger import logger

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False
    logger.warning("yt-dlp not installed. Install with: pip install yt-dlp")

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not installed. Install with: pip install openai")


class SimpleYouTubeProcessor:
    """Simple YouTube processor that extracts info, transcript, and description."""
    
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the YouTube processor.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.speech_processor = self.config.get("speech_processor")
        
        # YouTube download configuration
        self.ydl_opts = {
            'format': 'best[height<=720]/best',  # Fallback to any available format
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            # Add user agent to avoid 403 errors
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            # Add additional options to handle restrictions
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'no_color': True,
            # Try different extractors if one fails
            'extractor_retries': 3,
            'fragment_retries': 3,
            'retries': 3,
        }
        
        # OpenAI configuration for Whisper API
        self.openai_client = None
        if OPENAI_AVAILABLE:
            try:
                # Get OpenAI API key from environment or config
                api_key = os.getenv("OPENAI_API_KEY") or self.config.get("openai_api_key")
                base_url = os.getenv("OPENAI_BASE_URL") or self.config.get("openai_base_url")
                
                if api_key:
                    self.openai_client = openai.OpenAI(
                        api_key=api_key,
                        base_url=base_url
                    )
                    logger.info("✅ OpenAI client initialized for Whisper API")
                else:
                    logger.warning("⚠️ OpenAI API key not found, Whisper API will not be available")
                    
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize OpenAI client: {e}")
                self.openai_client = None
    
    def process(self, input_data: Union[str, Path, bytes], **kwargs) -> Dict[str, Any]:
        """
        Process YouTube URL and extract comprehensive content.
        
        Args:
            input_data: YouTube video URL (string)
            **kwargs: Additional processing parameters
            
        Returns:
            Dictionary containing extracted content and metadata
            
        Raises:
            Exception: If processing fails
        """
        if not YT_DLP_AVAILABLE:
            raise Exception("YouTube processing dependencies not available. Install yt-dlp: pip install yt-dlp")
        
        # Convert input_data to string if it's a Path
        url = str(input_data) if isinstance(input_data, Path) else input_data
        
        if not self._is_valid_youtube_url(url):
            raise Exception(f"Invalid YouTube URL: {url}")
        
        logger.info(f"Starting YouTube processing for: {url}")
        
        try:
            # Get video info
            video_info = self._get_video_info(url)
            
            # Get transcript if available
            transcript = self._get_transcript(url, video_info)
            
            # Get description
            description = video_info.get("description", "")
            
            # Create comprehensive text chunks
            text_chunks = self._create_text_chunks(video_info, transcript, description)
            
            logger.info(f"Completed YouTube processing for: {url}")
            logger.info(f"Generated {len(text_chunks)} text chunks")
            
            return {
                "text": text_chunks[0] if text_chunks else f"Video: {video_info.get('title', 'Unknown')} by {video_info.get('uploader', 'Unknown')}",
                "text_chunks": text_chunks,  # Multiple chunks for better embedding
                "metadata": video_info,
                "source": url,
                "type": "youtube",
                "duration": video_info.get("duration"),
                "title": video_info.get("title"),
                "author": video_info.get("uploader"),
                "view_count": video_info.get("view_count"),
                "upload_date": video_info.get("upload_date"),
                "transcript_available": transcript is not None,
                "description_length": len(description),
            }
            
        except Exception as e:
            logger.error(f"Error in YouTube processing: {e}")
            raise e
    
    def _is_valid_youtube_url(self, url: str) -> bool:
        """Check if URL is a valid YouTube URL."""
        youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
        parsed = urlparse(url)
        return any(domain in parsed.netloc for domain in youtube_domains)
    
    def _extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        parsed = urlparse(url)
        
        if 'youtube.com' in parsed.netloc:
            if parsed.path == '/watch':
                return parse_qs(parsed.query).get('v', [None])[0]
        elif 'youtu.be' in parsed.netloc:
            return parsed.path[1:]  # Remove leading slash
        
        return None
    
    def _get_video_info(self, url: str) -> Dict[str, Any]:
        """Get basic video info without downloading."""
        if not YT_DLP_AVAILABLE:
            raise Exception("YouTube processing dependencies not available")
        
        try:
            # Use the configured ydl_opts instead of basic config
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                logger.info(f"🔍 Extracting info for YouTube URL: {url}")
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    raise Exception("Failed to extract video info - no data returned")
                
                result = {
                    "title": info.get("title", "Unknown"),
                    "uploader": info.get("uploader", "Unknown"),
                    "duration": info.get("duration", 0),
                    "view_count": info.get("view_count", 0),
                    "upload_date": info.get("upload_date", ""),
                    "description": info.get("description", "")[:200],
                }
                
                logger.info(f"✅ Successfully extracted info: {result['title']} by {result['uploader']}")
                return result
                
        except Exception as e:
            error_msg = f"Failed to get video info for {url}: {e}"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def get_video_info(self, url: str) -> Dict[str, Any]:
        """Get video information without downloading."""
        return self._get_video_info(url)

    def _get_transcript(self, url: str, video_info: Dict[str, Any]) -> Optional[str]:
        """
        Get transcript from YouTube video using OpenAI Whisper API.
        
        Args:
            url: YouTube URL
            video_info: Video metadata
            
        Returns:
            Transcript text or None if not available
        """
        if not OPENAI_AVAILABLE or not self.openai_client:
            logger.warning("⚠️ OpenAI Whisper API not available for transcript generation")
            # vẫn cho phép dùng speech_processor nếu có
            if not self.speech_processor:
                logger.error("❌ No speech_processor provided; cannot generate transcript")
                return None
        
        try:
            # Check if video is too long (skip if > 20 minutes to avoid long processing)
            duration = video_info.get("duration", 0)
            if duration > 1200:  # 20 minutes
                logger.warning(f"⚠️ Video too long ({duration}s > 1200s), skipping transcript generation")
                return None
            
            logger.info(f"🎤 Generating transcript using STT for video (duration: {duration}s)...")
            
            # Download audio using yt-dlp
            audio_path = self._download_audio_only(url)
            if not audio_path:
                logger.error("❌ Audio download failed; cannot generate transcript")
                return None
            
            try:
                # Prefer centralized SpeechToTextProcessor if provided
                if self.speech_processor is not None:
                    stt_result = self.speech_processor.process(audio_path, use_openai_api=True, language=video_info.get("language"))
                    transcript_text = (stt_result or {}).get("text", "").strip()
                    if transcript_text:
                        logger.info(f"✅ Transcript generated via SpeechToTextProcessor: {len(transcript_text)} chars")
                        return transcript_text
                    logger.warning("⚠️ No transcript returned by SpeechToTextProcessor")
                    return None
                
                # Fallback: direct OpenAI client if configured
                if OPENAI_AVAILABLE and self.openai_client:
                    with open(audio_path, "rb") as audio_file:
                        transcript = self.openai_client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_file,
                            response_format="text"
                        )
                    if transcript:
                        logger.info(f"✅ Transcript generated via OpenAI API: {len(transcript)} characters")
                        return transcript.strip()
                
                logger.warning("⚠️ No transcript generated (no suitable STT path)")
                return None
            
            finally:
                # Clean up audio file
                if audio_path.exists():
                    audio_path.unlink()
                    
        except Exception as e:
            logger.error(f"❌ Failed to generate transcript via OpenAI API: {e}")
            return None
    
    def _download_audio_only(self, url: str) -> Optional[Path]:
        """
        Download only audio from YouTube video for transcript generation.
        Optimized for OpenAI Whisper API (supports mp3, mp4, mpeg, mpga, m4a, wav, webm).
        
        Args:
            url: YouTube URL
            
        Returns:
            Path to audio file or None if failed
        """
        try:
            # Use a dedicated temp directory and let yt-dlp manage filenames
            temp_dir = Path(tempfile.mkdtemp(prefix="yt_audio_"))
            logger.info(f"📥 Downloading audio for transcript generation into: {temp_dir}")
            
            audio_opts = self.ydl_opts.copy()
            audio_opts.update({
                # Prefer stable audio-only formats first (140=m4a, 251=webm opus)
                'format': '140/251/bestaudio',
                'outtmpl': '%(id)s.%(ext)s',
                'paths': {'home': str(temp_dir)},
                # Avoid postprocessing to reduce ffprobe/codec issues; OpenAI accepts m4a/webm directly
                'postprocessors': [],
                'noprogress': True,
                'overwrites': True,
                'concurrent_fragment_downloads': 1,
            })
            
            with yt_dlp.YoutubeDL(audio_opts) as ydl:
                ydl.download([url])
            
            # Collect candidate audio files
            candidates: List[Path] = []
            for pattern in ('*.m4a', '*.webm', '*.mp3', '*.wav', '*.mp4'):
                candidates.extend(temp_dir.glob(pattern))
            candidates = [p for p in candidates if p.exists() and p.stat().st_size > 0]
            
            if not candidates:
                logger.error("❌ Audio download failed - no audio file found in temp directory")
                return None
            
            # Pick the largest candidate as best quality
            best = max(candidates, key=lambda p: p.stat().st_size)
            size_mb = best.stat().st_size / (1024 * 1024)
            logger.info(f"✅ Audio downloaded successfully: {best.name} ({size_mb:.2f} MB)")
            return best
            
        except Exception as e:
            logger.error(f"❌ Failed to download audio: {e}")
            return None
    
    def _create_text_chunks(self, video_info: Dict[str, Any], transcript: Optional[str], description: str) -> List[str]:
        """
        Create multiple text chunks from video information.
        Optimized for better embedding and search capabilities.
        
        Args:
            video_info: Video metadata
            transcript: Video transcript
            description: Video description
            
        Returns:
            List of text chunks
        """
        chunks = []
        
        # Chunk 1: Basic video info (metadata)
        basic_info = f"Video: {video_info.get('title', 'Unknown')} by {video_info.get('uploader', 'Unknown')}. Duration: {video_info.get('duration', 0)} seconds. Upload date: {video_info.get('upload_date', 'Unknown')}. View count: {video_info.get('view_count', 0)}."
        chunks.append(basic_info)
        
        # Chunk 2: Description (if available and meaningful)
        if description:
            # Clean description (remove excessive whitespace, newlines)
            clean_description = " ".join(description.split())
            
            # Split description into chunks if too long
            desc_chunks = self._split_text_into_chunks(clean_description, max_length=400)
            chunks.extend(desc_chunks)
            logger.info(f"📝 Added {len(desc_chunks)} description chunks")
        
        # Chunk 3: Transcript (if available)
        if transcript:
            # Clean transcript (remove excessive whitespace, newlines)
            clean_transcript = " ".join(transcript.split())
            
            # Split transcript into chunks
            transcript_chunks = self._split_text_into_chunks(clean_transcript, max_length=400)
            chunks.extend(transcript_chunks)
            logger.info(f"🎤 Added {len(transcript_chunks)} transcript chunks")
        
        logger.info(f"📊 Total chunks created: {len(chunks)}")
        return chunks
    
    def _split_text_into_chunks(self, text: str, max_length: int = 400) -> List[str]:
        """
        Split text into chunks of specified length.
        Optimized for natural language boundaries and better embedding.
        
        Args:
            text: Text to split
            max_length: Maximum length of each chunk
            
        Returns:
            List of text chunks
        """
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        sentences = text.split('. ')
        
        current_chunk = ""
        
        for sentence in sentences:
            # Add period back if it's not the last sentence
            if sentence != sentences[-1]:
                sentence += "."
            
            # Check if adding this sentence would exceed max_length
            if len(current_chunk + " " + sentence) <= max_length:
                current_chunk += (" " + sentence) if current_chunk else sentence
            else:
                # Current chunk is full, save it and start new one
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        # Add the last chunk if it has content
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
