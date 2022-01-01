# Bookstack Shelf Exporter
_Exports all shelves of a bookstack instance as HTML, PDF or plaintext using python requests_

__Note:__ The API requires an administrator account on the bookstack instance.

## Installation

Clone this repository into a folder or download the `export.py` and `config.py` files.  
  
    git clone https://github.com/atlasax/bookstackexport.git bookstackexport/

## Configuration

Open the `config.py` with a text editor and fill in your settings:  
  
    BOOKSTACK_URL = "https://your.bookstackinstance.com"
    TOKEN_ID = "" # auth token id of an administrator
    TOKEN_SECRET = "" # auth token secret of an administrator
    EXPORT_ROOT = "exports/" # abs. or rel. path to export parent directory
    EXPORT_TYPE = "pdf" # choose: pdf, html, plaintext

The export will create a directory within the `EXPORT_ROOT` for each export.  
You can retrieve your token id & secret from an administrator's user page in your bookstack settings.

## Usage

Run the `export.py` file via `python3 export.py`. It will print a list of the fetched books and then ask for confirmation. The export will contain a folder for each shelf, each with all of the shelf's books as PDF/HTML/plaintext files.
