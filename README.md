# AssemblyAI Audio Transcript Loader

The AssemblyAI Audio Transcript Loader allows to transcribe audio files with the AssemblyAI API and loads the transcribed text into documents.

To use it, you should have the assemblyai python package installed, and the environment variable ASSEMBLYAI_API_KEY set with your API key. Alternatively, the API key can also be passed as an argument.

More info about AssemblyAI:

* (Website)[https://www.assemblyai.com/]
* (Get a Free API key)[https://www.assemblyai.com/dashboard/signup]
* (AssemblyAI API Docs)[https://www.assemblyai.com/docs]

## Installation

First, you need to install the assemblyai python package.

You can find more info about it inside the assemblyai-python-sdk GitHub repo.

```
pip install assemblyai
```

## Usage

The `AssemblyAITranscriber` needs to be initialized with the AssemblyAI API key. 
The `run` function needs at least the file_path argument. Audio files can be specified as an URL or a local file path.]
You can also specify whether you want summarization and speaker diarization results in the `run` function.

```
from assemblyai_haystack.transcriber import AssemblyAITranscriber
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack import Pipeline
from haystack.components.writers import DocumentWriter

ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY")

## Use AssemblyAITranscriber in a pipeline
document_store = InMemoryDocumentStore()
file_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

indexing = Pipeline()
indexing.add_component("transcriber", AssemblyAITranscriber(api_key=ASSEMBLYAI_API_KEY))
indexing.add_component("writer", DocumentWriter(document_store))
indexing.connect("transcriber.transcription", "writer.documents")
indexing.run(
    {
        "transcriber": {
            "file_path": file_url,
            "summarization": None,
            "speaker_labels": None,
        }
    }
)

print("Indexed Document Count:", document_store.count_documents())
```

Note: Calling `indexing.run()` blocks until the transcription is finished.

The results of the transcription, summarization and speaker diarization are returned in separate document lists:
* transcription
* summarization
* speaker_labels

The metadata of the transcription document contains the transcription ID and url of the uploaded audio file.

docs[0].metadata
# {'transcript_id': '	73089e32-...-4ae9-97a4-eca7fe20a8b1',
#  'audio_url': 'https://storage.googleapis.com/aai-docs-samples/nbc.mp3',
# }
  
