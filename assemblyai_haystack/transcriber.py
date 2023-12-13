from typing import Dict, List, Any, Optional

from haystack import component, Document
from haystack.lazy_imports import LazyImport

with LazyImport(message="Run 'pip install assemblyai'") as assemblyai_import:
    import assemblyai as aai

@component
class AssemblyAITranscriber:
    def __init__(self, *, api_key: Optional[str] = None):
        assemblyai_import.check()

        if api_key is not None:
            aai.settings.api_key = api_key

    @component.output_types(
        transcription=List[Document],
        summarization=List[Document],
        speaker_labels=List[Document],
    )
    def run(
        self,
        file_path: str,
        summarization: bool = False,
        speaker_labels: bool = False,
    ):
        config = aai.TranscriptionConfig(
            speaker_labels=speaker_labels, summarization=summarization
        )

        # Instantiating the Transcriber will raise a ValueError if no API key is set.
        self.transcriber = aai.Transcriber(config=config)
        transcript = self.transcriber.transcribe(file_path)

        # Not doing TypeChecking here because there is only one type of Transcript Format
        if transcript.error:
            raise ValueError(f"Could not transcribe file: {transcript.error}")


        summarization_doc = {}
        # Create summarization result doc
        if config.summarization:
            summarization_doc = {
                "summarization": [Document(content=transcript.summary)]
            }
        
        speakers_doc = {}
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