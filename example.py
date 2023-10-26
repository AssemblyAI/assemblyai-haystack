import os

from assemblyai_haystack.transcriber import AssemblyAITranscriber
from haystack.preview.document_stores import MemoryDocumentStore
from haystack.preview import Pipeline
from haystack.preview.components.writers import DocumentWriter

ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY")

## Use AssemblyAITranscriber in a pipeline

document_store = MemoryDocumentStore()

indexing = Pipeline()
indexing.add_component("transcriber", AssemblyAITranscriber(api_key=ASSEMBLYAI_API_KEY))
indexing.add_component("writer", DocumentWriter(document_store))
indexing.connect("transcriber", "writer")
indexing.run({"transcriber": {"file_url": "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3", "speaker_labels":True}})

print("Indexed Document Count:", document_store.count_documents())

## Use AssemblyAITranscriber as a stand alone component
# transcript = transcriber.run(file_url="https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3", speaker_labels=True)

