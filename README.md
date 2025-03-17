# ArchiveBookDownloader

A powerful utility to download books from Archive.org with PDF conversion and Google Drive integration.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/abdullah-elbedwehy/ArchiveBookDownloader/blob/main/ArchiveBookDownloader.ipynb)

## Features

- Download books from Archive.org with a simple URL
- Multi-threaded downloads for faster performance
- Convert downloaded images to a single PDF
- Configurable image resolution
- Option to save metadata
- Google Drive integration for Colab users with shareable links
- Support for returning loans automatically

## Requirements

- Archive.org account with borrowing privileges (create one at https://archive.org/account/signup)
- Valid login credentials for Archive.org
- Python 3.6+
- Required packages:
  - requests
  - futures
  - tqdm
  - img2pdf (for PDF conversion)
  - Google Colab libraries (for Google Drive integration)

## Installation

### Local Installation

1. Clone this repository:
```bash
git clone https://github.com/USERNAME/ArchiveBookDownloader.git
cd ArchiveBookDownloader
```

2. Install required packages:
```bash
pip install requests futures tqdm img2pdf
```

### Google Colab

Simply click the "Open in Colab" button at the top of this README and run the notebook in Google Colab.

## Usage

### Configuration

Before using the tool, you need to configure your Archive.org credentials:

1. Open `ArchiveBookDownloader.py` (or use the Colab notebook)
2. Replace the hardcoded EMAIL and PASSWORD values with your Archive.org credentials:

```python
EMAIL = "your_email@example.com"
PASSWORD = "your_password"
```

### Settings

You can customize these settings:

- `RESOLUTION`: Image resolution (0-10, where 0 is highest quality)
- `N_THREADS`: Maximum number of download threads
- `CREATE_PDF`: Set to True to create a PDF, False to keep individual JPGs
- `SAVE_METADATA`: Set to True to save book metadata
- `SAVE_TO_GDRIVE`: Set to True to save to Google Drive (Colab only)
- `OUTPUT_DIR`: Directory to save downloads

### Running the Tool

#### Local Python Script
```bash
python ArchiveBookDownloader.py
```
You'll be prompted to enter an Archive.org book URL.

#### Google Colab
Run all cells in the notebook and follow the prompts.

## How it Works

1. The tool authenticates with your Archive.org account
2. It borrows the book if necessary
3. All book pages are downloaded as images
4. Images are converted to a single PDF (if enabled)
5. The book is returned automatically
6. With Google Drive integration, a shareable link is created

## Important Notes

- This tool requires an Archive.org account
- Respect copyright and usage terms on Archive.org
- Some books may not be available for borrowing

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Internet Archive for their amazing service
- The open-source community for the libraries used in this project 