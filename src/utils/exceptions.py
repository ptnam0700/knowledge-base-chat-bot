"""
Custom exceptions for Thunderbolts application.
"""


class ThunderboltsException(Exception):
    """Base exception for Thunderbolts application."""
    pass


class FileProcessingError(ThunderboltsException):
    """Exception raised when file processing fails."""
    pass


class AudioProcessingError(ThunderboltsException):
    """Exception raised when audio processing fails."""
    pass


class VideoProcessingError(ThunderboltsException):
    """Exception raised when video processing fails."""
    pass


class TextProcessingError(ThunderboltsException):
    """Exception raised when text processing fails."""
    pass


class SpeechToTextError(ThunderboltsException):
    """Exception raised when speech-to-text conversion fails."""
    pass


class EmbeddingError(ThunderboltsException):
    """Exception raised when embedding generation fails."""
    pass


class VectorDatabaseError(ThunderboltsException):
    """Exception raised when vector database operations fail."""
    pass


class SearchError(ThunderboltsException):
    """Exception raised when search operations fail."""
    pass


class WebSearchError(ThunderboltsException):
    """Exception raised when web search fails."""
    pass


class LLMError(ThunderboltsException):
    """Exception raised when LLM operations fail."""
    pass


class ConfigurationError(ThunderboltsException):
    """Exception raised when configuration is invalid."""
    pass


class UnsupportedFormatError(ThunderboltsException):
    """Exception raised when file format is not supported."""
    pass


class FileSizeError(ThunderboltsException):
    """Exception raised when file size exceeds limits."""
    pass


class TTSProcessingError(ThunderboltsException):
    """Exception raised when text-to-speech processing fails."""
    pass
