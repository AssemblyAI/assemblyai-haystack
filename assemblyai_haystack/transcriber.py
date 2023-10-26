from typing import TYPE_CHECKING, Dict, List, Any, Optional, Union
from pathlib import Path

from enum import Enum

from canals.serialization import default_to_dict, default_from_dict
from haystack.preview import component, Document

if TYPE_CHECKING:
    import assemblyai

class TranscriptFormat(Enum):
    """Transcript format to use for the document reader."""

    TEXT = "text"
    """One document with the transcription text"""


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
        transcript_format: TranscriptFormat = TranscriptFormat.TEXT,
        speaker_labels: Optional[bool] = None,
        iab_categories: Optional[bool] = None,
        config: Optional[assemblyai.TranscriptionConfig] = None,
        ):

        self.file_path = file_path
        self.transcript_format = transcript_format

        # Instantiating the Transcriber will raise a ValueError if no API key is set.
        self.transcriber = assemblyai.Transcriber(config=config, speaker_labels=speaker_labels, iab_categories=iab_categories)
    
        transcript = self.transcriber.transcribe(self.file_path)

        if transcript.error:
            raise ValueError(f"Could not transcribe file: {transcript.error}")

        # transcript of the audio or the video file is returned by default
        if self.transcript_format == TranscriptFormat.TEXT:
            transcription_doc = {"transcription": [
                Document(text=transcript.text, 
                         metadata=transcript.json_response)
                ]}
            
            ''' Speaker labels or the iab categories can be turned on or off '''
            if self.speaker_labels:
                speaker_labels_doc = {"speakers" : [
                    Document(text=utterance.text, 
                             metadata={"speaker": utterance.speaker, 
                                       "details":utterance.dict(exclude={"text"})})
                    for utterance in transcript.utterances
                ]}
            else:
                speaker_labels_doc = {"speakers" : []}
                
            """This is what the "labels" would look like
                            
            [IABLabelResult(relevance=0.5121853351593018, label='Education>LanguageLearning'), 
            IABLabelResult(relevance=0.2464590072631836, label='Technology&Computing>ArtificialIntelligence'), 
            IABLabelResult(relevance=0.02066299505531788, label='FamilyAndRelationships>Parenting>ParentingBabiesAndToddlers')]"""
            if self.iab_categories:
                iab_categories_doc = {"topics" : [
                    Document(text=result.text, 
                             metadata={"labels": result.labels, 
                                       "details":result.dict(exclude={"text"})})
                    for result in transcript.iab_categories.results
                             ]}
            else:
                iab_categories_doc = {"topics" : []}

        else:
            raise ValueError("Unknown transcript format.")

        # ToDos:
        # add utterance number to metadata?
        # think of different ways to return the speaker diarization output
        # based on which models are running, change key in the dictionary

        # speech rec., speaker diarization, topic detection

        results = {**transcription_doc, **speaker_labels_doc, **iab_categories_doc} 
        return results