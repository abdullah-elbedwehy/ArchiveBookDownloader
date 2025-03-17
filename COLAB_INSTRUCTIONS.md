# Using ArchiveBookDownloader in Google Colab

This guide will help you use ArchiveBookDownloader in Google Colab.

## Steps to Run in Google Colab

1. Open Google Colab: [https://colab.research.google.com/](https://colab.research.google.com/)

2. Create a new notebook

3. In the first cell, install the required packages:
   ```python
   !pip install requests tqdm img2pdf
   ```

4. In the next cell, copy and paste the entire content of the `ArchiveBookDownloader_colab.py` file from this repository

5. Edit the following variables with your information:
   ```python
   # Replace these with your own Archive.org credentials
   EMAIL = "your_email@example.com"
   PASSWORD = "your_password"
   ```

6. Run all cells in the notebook. You'll be prompted to enter an Archive.org book URL.

7. If you have enabled Google Drive integration (`SAVE_TO_GDRIVE = True`), you'll need to authorize access when prompted.

8. After the download completes, a clickable link to your PDF will be displayed.

## Troubleshooting

- If you encounter errors related to authentication, make sure your Archive.org credentials are correct.
- If the PDF creation fails, check if the `img2pdf` package is properly installed.
- If Google Drive integration isn't working, ensure you have authorized access when prompted.

## Alternative Method

You can also directly open our pre-configured Colab notebook by clicking this link:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/abdullah-elbedwehy/ArchiveBookDownloader/blob/main/ArchiveBookDownloader.ipynb)

This pre-configured notebook has everything set up - you just need to add your credentials and run the cells! 