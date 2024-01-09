<img src="https://github.com/AssemblyAI/assemblyai-python-sdk/blob/master/assemblyai.png?raw=true" width="500"/>

---


[![CI Passing](https://github.com/AssemblyAI/assemblyai-python-sdk/actions/workflows/test.yml/badge.svg)](https://github.com/AssemblyAI/assemblyai-haystack/actions/workflows/test.yml)
[![GitHub License](https://img.shields.io/github/license/AssemblyAI/assemblyai-haystack)](https://github.com/AssemblyAI/assemblyai-haystack/blob/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/assemblyai-haystack.svg)](https://badge.fury.io/py/assemblyai-haystack)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/assemblyai-haystack)](https://pypi.python.org/pypi/assemblyai-haystack/)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/assemblyai-haystack)
[![AssemblyAI Twitter](https://img.shields.io/twitter/follow/AssemblyAI?label=%40AssemblyAI&style=social)](https://twitter.com/AssemblyAI)
[![AssemblyAI YouTube](https://img.shields.io/youtube/channel/subscribers/UCtatfZMf-8EkIwASXM4ts0A)](https://www.youtube.com/@AssemblyAI)
[![Discord](https://img.shields.io/discord/875120158014853141?logo=discord&label=Discord&link=https%3A%2F%2Fdiscord.com%2Fchannels%2F875120158014853141&style=social)
](https://assemblyai.com/discord)

# AssemblyAI Audio Transcript Loader

The AssemblyAI Audio Transcript Loader allows to transcribe audio files with the AssemblyAI API and loads the transcribed text into documents.

To use it, you should have the environment variable ASSEMBLYAI_API_KEY set with your API key. Alternatively, the API key can also be passed as an argument.

More info about AssemblyAI:

* [Website](https://www.assemblyai.com/)
* [Get a Free API key](https://www.assemblyai.com/dashboard/signup)
* [AssemblyAI API Docs](https://www.assemblyai.com/docs)

## Installation

First, install the assemblyai-haystack python package.

```bash
pip install assemblyai-haystack
```

This package installs and uses the AssemblyAI Python SDK. You can find more info about the SDK at the [assemblyai-python-sdk GitHub repo]([https://www.assemblyai.com/docs](https://github.com/AssemblyAI/assemblyai-python-sdk)).

## Usage

The `AssemblyAITranscriber` needs to be initialized with the AssemblyAI API key. 
The `run` function needs at least the file_path argument. Audio files can be specified as an URL or a local file path.
You can also specify whether you want summarization and speaker diarization results in the `run` function.

```python
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

```json
{
   "transcript_id":"73089e32-...-4ae9-97a4-eca7fe20a8b1",
   "audio_url":"https://storage.googleapis.com/aai-docs-samples/nbc.mp3"
}
```
  
