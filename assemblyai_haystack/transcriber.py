from typing import TYPE_CHECKING, Dict, List, Any, Optional, Union
from pathlib import Path

from enum import Enum

from canals.serialization import default_to_dict, default_from_dict
from haystack.preview import component, Document

# if TYPE_CHECKING:
import assemblyai


@component
class AssemblyAITranscriber:
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
    ):
        try:
            import assemblyai
        except ImportError:
            raise ImportError(
                "Could not import assemblyai python package. "
                "Please install it with `pip install assemblyai`."
            )
        if api_key is not None:
            assemblyai.settings.api_key = api_key

    def to_dict(self) -> Dict[str, Any]:
        return default_to_dict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AssemblyAITranscriber":
        return default_from_dict(cls, data)
        
    @component.output_types(documents=List[Document])    
    def run(
        self,
        file_path: str,
        # transcript_format: TranscriptFormat = TranscriptFormat.TEXT,
        config: Optional[assemblyai.TranscriptionConfig] = None,
        ):

        self.file_path = file_path
        # self.transcript_format = transcript_format

        # Instantiating the Transcriber will raise a ValueError if no API key is set.
        self.transcriber = assemblyai.Transcriber(config=config)
        transcript = self.transcriber.transcribe(self.file_path)

        ''' Not doing TypeChecking here because there is only one type of Transcript Format '''

        if transcript.error:
            raise ValueError(f"Could not transcribe file: {transcript.error}")

        transcript_json = transcript.json_response

        ''' Higher level keys cannot be used in the metadata '''
        transcript_json["transcription_id"] = transcript_json.pop("id")
        transcript_json["transcription_text"] = transcript_json.pop("text")

        transcription_doc = {"transcription": [
            Document(text=transcript.text, 
                        metadata=transcript_json)
            ]}
    

        results = {**transcription_doc} 
        return results