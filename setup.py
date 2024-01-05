from pathlib import Path

from setuptools import find_packages, setup

long_description = (Path(__file__).parent / "README.md").read_text()


setup(
    name="assemblyai",
    version="0.20.2",
    description="AssemblyAI Haystack Integration",
    author="AssemblyAI",
    author_email="marketing@assemblyai.com",
    packages=find_packages(),
    install_requires=[
        "haystack-ai>=0.137.0",
        "assemblyai>=0.18.0",
    ],
    extras_require={
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache License 2.0",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AssemblyAI/assemblyai-haystack",
    license="Apache License 2.0",
    license_files=["LICENSE"],
    python_requires=">=3.8",
    project_urls={
        "Code": "https://github.com/AssemblyAI/assemblyai-haystack",
        "Issues": "https://github.com/AssemblyAI/assemblyai-haystack/issues",
        "Documentation": "https://github.com/AssemblyAI/assemblyai-haystack/blob/main/README.md",
        "API Documentation": "https://www.assemblyai.com/docs/",
        "Website": "https://assemblyai.com/",
    },
)
