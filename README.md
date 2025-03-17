# ArchiveBookDownloader

A powerful utility to download books from Archive.org with PDF conversion and Google Drive integration.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/abdullah-elbedwehy/ArchiveBookDownloader/blob/main/ArchiveBookDownloader_colab.ipynb)

## Features

- Download books from Archive.org with a simple URL
- Multi-threaded downloads for faster performance
- Convert downloaded images to a single PDF
- Configurable image resolution
- Option to save metadata
- Google Drive integration for Colab users with shareable links
- Support for returning loans automatically

## Getting Started

### Creating an Archive.org Account

1. Visit [Archive.org](https://archive.org/account/signup)
2. Click on "Sign Up" in the top right corner
3. Fill in your email address, username, and password
4. Verify your email address by clicking the link sent to you
5. Your account is now ready to use for borrowing books!

### Choose Your Method

You can use ArchiveBookDownloader in two ways:

1. **Google Colab (Recommended for beginners)**: Run in the cloud without any installation on your computer
2. **Local Installation**: Run on your own computer (requires Python setup)

## Option 1: Google Colab (Easiest Method)

1. Click the "Open in Colab" button at the top of this README
2. When the notebook opens in Google Colab, click "Runtime" in the menu, then "Run all"
3. Enter your Archive.org email and password when prompted
4. Enter the URL of the book you want to download
5. The book will be downloaded and converted to PDF
6. If you enable Google Drive integration, a shareable link will be created

### Detailed Colab Instructions:

1. When you first run the notebook, you'll be asked to connect to Google Drive - click "Connect to Google Drive"
2. Follow the authentication steps
3. The notebook will create a folder called "ArchiveBookDownloader" in your Google Drive
4. Enter your Archive.org login details in the configuration cell
5. Enter the book URL in the format: `https://archive.org/details/book_id`
6. The downloaded PDF will be saved to your Google Drive

## Option 2: Local Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Installation Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/abdullah-elbedwehy/ArchiveBookDownloader.git
   cd ArchiveBookDownloader
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Open the Jupyter notebook:
   ```bash
   jupyter notebook ArchiveBookDownloader_local.ipynb
   ```
   
   If you don't have Jupyter installed, install it first:
   ```bash
   pip install jupyter
   ```

4. Follow the instructions in the notebook:
   - Enter your Archive.org credentials
   - Set your desired configuration options
   - Enter the URL of the book you want to download
   - Run all cells in the notebook

## How to Find Books on Archive.org

1. Go to [Archive.org](https://archive.org/)
2. Use the search bar to find books by title, author, subject, etc.
3. Look for books that have a "Borrow" button - these are the ones you can download
4. Click on the book to view its details
5. Copy the URL from your browser's address bar
6. Paste this URL into the ArchiveBookDownloader notebook

## Troubleshooting

### Common Issues:

- **Invalid credentials**: Double-check your Archive.org email and password
- **Book not available**: Some books may not be available for borrowing
- **Download errors**: If download fails, try reducing the number of threads
- **PDF creation fails**: This might happen with very large books or corrupted images

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is intended for educational purposes and personal use only. Please respect copyright laws and the terms of service of Archive.org.