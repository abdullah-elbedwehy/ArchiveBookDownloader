import requests
import random, string
from concurrent import futures
from tqdm import tqdm
import time
from datetime import datetime
import os
import sys
import shutil
import json
import warnings
import logging

# Suppress urllib3 warnings
logging.getLogger("urllib3").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning)

# Hardcoded credentials - REPLACE THESE WITH YOUR OWN
EMAIL = "56db6c2938@emaily.pro"
PASSWORD = "56db6c2938@emaily.pro"

# settings
RESOLUTION = 0  # Image resolution (10 to 0, 0 is the highest)
N_THREADS = 50  # Maximum number of threads
CREATE_PDF = True  # Whether to create a PDF (True) or keep individual JPGs (False)
SAVE_METADATA = False  # Whether to save metadata
SAVE_TO_GDRIVE = True  # Whether to save to Google Drive and create a shareable link (requires permission)
OUTPUT_DIR = os.getcwd()  # Current directory (change it to your desired directory) example: "C:\Users\YourName\Downloads\archive.org"

def display_error(response, message):
	print(message)
	print(response)
	print(response.text)
	exit()

def get_book_infos(session, url):
	r = session.get(url).text
	infos_url = "https:" + r.split('"url":"')[1].split('"')[0].replace("\\u0026", "&")
	response = session.get(infos_url)
	data = response.json()['data']
	title = data['brOptions']['bookTitle'].strip().replace(" ", "_")
	title = ''.join( c for c in title if c not in '<>:"/\\|?*' ) # Filter forbidden chars in directory names (Windows & Linux)
	title = title[:150] # Trim the title to avoid long file names	
	metadata = data['metadata']
	links = []
	for item in data['brOptions']['data']:
		for page in item:
			links.append(page['uri'])

	if len(links) > 1:
		print(f"[+] Found {len(links)} pages")
		return title, links, metadata
	else:
		print(f"[-] Error while getting image links")
		exit()

def login(email, password):
	session = requests.Session()
	session.get("https://archive.org/account/login")

	data = {"username":email, "password":password}

	response = session.post("https://archive.org/account/login", data=data)
	if "bad_login" in response.text:
		print("[-] Invalid credentials! Please update the EMAIL and PASSWORD variables in the script.")
		exit()
	elif "Successful login" in response.text:
		print("[+] Successful login")
		return session
	else:
		display_error(response, "[-] Error while login:")

def loan(session, book_id, verbose=True):
	data = {
		"action": "grant_access",
		"identifier": book_id
	}
	response = session.post("https://archive.org/services/loans/loan/searchInside.php", data=data)
	data['action'] = "browse_book"
	response = session.post("https://archive.org/services/loans/loan/", data=data)

	if response.status_code == 400 :
		if response.json()["error"] == "This book is not available to borrow at this time. Please try again later.":
			print("This book doesn't need to be borrowed")
			return session
		else :
			display_error(response, "Something went wrong when trying to borrow the book.")

	data['action'] = "create_token"
	response = session.post("https://archive.org/services/loans/loan/", data=data)

	if "token" in response.text:
		if verbose:
			print("[+] Successful loan")
		return session
	else:
		display_error(response, "Something went wrong when trying to borrow the book, maybe you can't borrow this book.")

def return_loan(session, book_id):
	data = {
		"action": "return_loan",
		"identifier": book_id
	}
	response = session.post("https://archive.org/services/loans/loan/", data=data)
	if response.status_code == 200 and response.json()["success"]:
		print("[+] Book returned")
	else:
		display_error(response, "Something went wrong when trying to return the book")

def image_name(pages, page, directory):
	return f"{directory}/{(len(str(pages)) - len(str(page))) * '0'}{page}.jpg"

def download_one_image(session, link, i, directory, book_id, pages):
	headers = {
		"Referer": "https://archive.org/",
		"Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
		"Sec-Fetch-Site": "same-site",
		"Sec-Fetch-Mode": "no-cors",
		"Sec-Fetch-Dest": "image",
	}
	retry = True
	while retry:
		try:
			response = session.get(link, headers=headers)
			if response.status_code == 403:
				session = loan(session, book_id, verbose=False)
				raise Exception("Borrow again")
			elif response.status_code == 200:
				retry = False
		except:
			time.sleep(1)	# Wait 1 second before retrying

	image = image_name(pages, i, directory)
	with open(image,"wb") as f:
		f.write(response.content)


def download(session, n_threads, directory, links, scale, book_id):
	print("Downloading pages...")
	links = [f"{link}&rotate=0&scale={scale}" for link in links]
	pages = len(links)

	tasks = []
	with futures.ThreadPoolExecutor(max_workers=n_threads) as executor:
		for link in links:
			i = links.index(link)
			tasks.append(executor.submit(download_one_image, session=session, link=link, i=i, directory=directory, book_id=book_id, pages=pages))
		for task in tqdm(futures.as_completed(tasks), total=len(tasks)):
			pass
	
	images = [image_name(pages, i, directory) for i in range(len(links))]
	return images

def create_shareable_link(file_path):
	"""
	Creates a shareable link for a file in Google Colab
	
	Args:
		file_path (str): Path to the file
		
	Returns:
		str: Shareable URL for the file or local path if not using Google Drive
	"""
	# If not configured to use Google Drive, return local path
	if not SAVE_TO_GDRIVE:
		print("[!] Google Drive saving is disabled. File saved locally.")
		return f"File saved locally at: {file_path}"
		
	try:
		# Check if running in Google Colab
		import google.colab
		from google.colab import drive
		from google.colab import files
		
		print("[+] Creating shareable link using Google Drive...")
		print("[!] Note: This requires permission to access your Google Drive")
		
		# Mount Google Drive if not already mounted
		drive_mounted = os.path.exists('/content/drive')
		if not drive_mounted:
			print("[+] Mounting Google Drive... (You'll need to authorize access)")
			drive.mount('/content/drive')
		
		# Create a directory in Google Drive for archive.org books if it doesn't exist
		drive_dir = '/content/drive/MyDrive/archive.org'
		os.makedirs(drive_dir, exist_ok=True)
		
		# Copy the file to Google Drive
		file_name = os.path.basename(file_path)
		drive_file_path = os.path.join(drive_dir, file_name)
		shutil.copy2(file_path, drive_file_path)
		print(f"[+] File copied to Google Drive: {drive_file_path}")
		
		# Use Google Drive API to get file ID and create shareable link
		from google.colab import auth
		from googleapiclient.discovery import build
		from googleapiclient.http import MediaFileUpload
		
		# Authenticate
		auth.authenticate_user()
		
		# Build the Drive API service
		drive_service = build('drive', 'v3')
		
		# Create Drive API compatible path
		folder_name = 'archive.org'
		
		# First, check if our folder exists
		folders = drive_service.files().list(
			q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
			spaces='drive',
			fields='files(id, name)'
		).execute().get('files', [])
		
		# If folder doesn't exist, create it
		if not folders:
			folder_metadata = {
				'name': folder_name,
				'mimeType': 'application/vnd.google-apps.folder'
			}
			folder = drive_service.files().create(
				body=folder_metadata, fields='id'
			).execute()
			folder_id = folder.get('id')
		else:
			folder_id = folders[0]['id']
		
		# Upload the file directly through the API
		file_metadata = {
			'name': file_name,
			'parents': [folder_id]
		}
		
		media = MediaFileUpload(
			file_path, 
			mimetype='application/pdf',
			resumable=True
		)
		
		file = drive_service.files().create(
			body=file_metadata,
			media_body=media,
			fields='id'
		).execute()
		
		file_id = file.get('id')
		
		# Make the file publicly accessible
		drive_service.permissions().create(
			fileId=file_id,
			body={'type': 'anyone', 'role': 'reader'},
			fields='id'
		).execute()
		
		# Create shareable link
		shareable_link = f"https://drive.google.com/file/d/{file_id}/view"
		print(f"[+] Shareable link created: {shareable_link}")
		return shareable_link
		
	except ImportError:
		# Not running in Colab, use direct file path
		print("[!] Not running in Google Colab. File saved locally.")
		return f"File saved locally at: {file_path}"
	except Exception as e:
		print(f"[-] Error creating shareable link: {str(e)}")
		print("[!] File saved locally instead.")
		return f"File saved locally at: {file_path}"

def make_pdf(pdf, title, directory):
	file = title+".pdf"
	# Handle the case where multiple books with the same name are downloaded
	i = 1
	while os.path.isfile(os.path.join(directory, file)):
		file = f"{title}({i}).pdf"
		i += 1

	file_path = os.path.join(directory, file)
	with open(file_path, "wb") as f:
		f.write(pdf)
	print(f"[+] PDF saved as \"{file}\"")
	return file_path

def download_book(url):
	"""
	Main function to download a book from archive.org
	
	Args:
		url (str): URL of the book (must start with https://archive.org/details/)
	
	Returns:
		tuple: (success, shareable_link) - Whether the download was successful and the shareable link if applicable
	"""
	if not url.startswith("https://archive.org/details/"):
		print("Invalid URL. URL must start with \"https://archive.org/details/\"")
		return False, None

	session = login(EMAIL, PASSWORD)
	
	book_id = list(filter(None, url.split("/")))[3]
	print("="*40)
	print(f"Current book: https://archive.org/details/{book_id}")
	
	session = loan(session, book_id)
	title, links, metadata = get_book_infos(session, url)

	directory = os.path.join(OUTPUT_DIR, title)
	# Handle the case where multiple books with the same name are downloaded
	i = 1
	_directory = directory
	while os.path.isdir(directory):
		directory = f"{_directory}({i})"
		i += 1
	os.makedirs(directory)
	
	if SAVE_METADATA:
		print("Writing metadata.json...")
		with open(f"{directory}/metadata.json",'w') as f:
			json.dump(metadata,f)

	images = download(session, N_THREADS, directory, links, RESOLUTION, book_id)
	shareable_link = None

	if CREATE_PDF:  # Create pdf with images and remove the images folder
		try:
			import img2pdf
			
			# prepare PDF metadata
			# sometimes archive metadata is missing
			pdfmeta = { }
			# ensure metadata are str
			for key in ["title", "creator", "associated-names"]:
				if key in metadata:
					if isinstance(metadata[key], str):
						pass
					elif isinstance(metadata[key], list):
						metadata[key] = "; ".join(metadata[key])
					else:
						raise Exception("unsupported metadata type")
			# title
			if 'title' in metadata:
				pdfmeta['title'] = metadata['title']
			# author
			if 'creator' in metadata and 'associated-names' in metadata:
				pdfmeta['author'] = metadata['creator'] + "; " + metadata['associated-names']
			elif 'creator' in metadata:
				pdfmeta['author'] = metadata['creator']
			elif 'associated-names' in metadata:
				pdfmeta['author'] = metadata['associated-names']
			# date
			if 'date' in metadata:
				try:
					pdfmeta['creationdate'] = datetime.strptime(metadata['date'][0:4], '%Y')
				except:
					pass
			# keywords
			pdfmeta['keywords'] = [f"https://archive.org/details/{book_id}"]

			pdf = img2pdf.convert(images, **pdfmeta)
			pdf_file_path = make_pdf(pdf, title, OUTPUT_DIR)
			
			# Create shareable link for the PDF
			shareable_link = create_shareable_link(pdf_file_path)
			
			try:
				shutil.rmtree(directory)
			except OSError as e:
				print ("Error: %s - %s." % (e.filename, e.strerror))
		except ImportError:
			print("[-] img2pdf module not found. Please install it with 'pip install img2pdf'")
			print("[+] Images saved in directory:", directory)
			return False, None

	return_loan(session, book_id)
	return True, shareable_link

if __name__ == "__main__":
	# Display information about Google Drive integration if enabled
	if SAVE_TO_GDRIVE:
		print("=" * 60)
		print("NOTICE: This script will save files to Google Drive if running in Colab")
		print("You will need to authorize access to your Google Drive when prompted")
		print("Files will be saved in the 'archive.org' folder in your Drive")
		print("=" * 60)
		
	url = input("Enter archive.org book URL: ").strip()
	success, shareable_link = download_book(url)
	
	if success and shareable_link:
		print("\n" + "="*40)
		print("Download complete!")
		
		# Display clickable link in Colab
		try:
			from IPython.display import HTML, display
			from google.colab import output
			
			# Create a clickable link
			html_link = f'<h3>📚 <a href="{shareable_link}" target="_blank">Click here to view the PDF</a></h3>'
			display(HTML(html_link))
			
			# Also print the raw link as backup
			print(f"Or use this link: {shareable_link}")
		except ImportError:
			# Not in Colab or IPython environment
			print(f"Online link to access the book: {shareable_link}")
		
		print("="*40)