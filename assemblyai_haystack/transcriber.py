from typing import Dict, List, Any, Optional

from canals.serialization import default_to_dict, default_from_dict
from haystack.preview import component, Document

from haystack.lazy_imports import LazyImport

with LazyImport(message="Run 'pip install assemblyai'") as assemblyai_import:
    import assemblyai as aai

@component
class AssemblyAITranscriber:
    def __init__(self, *, api_key: Optional[str] = None):
        assemblyai_import.check()

        if api_key is not None:
            aai.settings.api_key = api_key

    def to_dict(self) -> Dict[str, Any]:
        return default_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AssemblyAITranscriber":
        return default_from_dict(cls, data)

    @component.output_types(
        transcription=List[Document],
        summarization=List[Document],
        speaker_labels=List[Document],
    )
    def run(
        self,
        file_path: str,
        summarization: Optional[bool] = False,
        speaker_labels: Optional[bool] = False,
    ):
        self.file_path = file_path

        config = aai.TranscriptionConfig(
            speaker_labels=speaker_labels, summarization=summarization
        )

        # Instantiating the Transcriber will raise a ValueError if no API key is set.
        self.transcriber = aai.Transcriber(config=config)
        transcript = self.transcriber.transcribe(self.file_path)

        # Not doing TypeChecking here because there is only one type of Transcript Format
        if transcript.error:
            raise ValueError(f"Could not transcribe file: {transcript.error}")

        # Create summarization result doc
        if config.summarization:
            summarization_doc = {
                "summarization": [Document(content=transcript.summary)]
            }
        else:
            summarization_doc = {}

        # create speaker labels result doc
        if config.speaker_labels:
            speakers_doc = {
                "speaker_labels": [
                    Document(
                        content=utterance.text, meta={"speaker": utterance.speaker}
                    )
                    for utterance in transcript.utterances
                ]
            }
        else:
            speakers_doc = {}

        # create transcription result doc
        transcription_doc = {
            "transcription": [
                Document(
                    content=transcript.text,
                    meta={
                        "transcript_id": transcript.id,
                        "audio_url": transcript.audio_url,
                    },
                )
            ]
        }

        results = {**transcription_doc, **summarization_doc, **speakers_doc}
        return results