#!/usr/bin/env python3

import config
import requests, json, os, os.path
from datetime import datetime

HEADER = { 'Authorization': f'Token {config.TOKEN_ID}:{config.TOKEN_SECRET}' }
SHELVES_URL = f'{config.BOOKSTACK_URL}/api/shelves'
BOOKS_URL = f'{config.BOOKSTACK_URL}/api/books'

# Fetch all available shelves

print('Fetching shelves...')

shelves_resp = requests.get(SHELVES_URL, headers=HEADER)
shelves = json.loads(json.dumps(shelves_resp.json(), separators=[',',':']))['data']

# Fetch all available books per shelf

books = {}
for shelf_header in shelves:
    shelf_resp = requests.get(f'{SHELVES_URL}/{shelf_header["id"]}', headers=HEADER)
    shelf = json.loads(json.dumps(shelf_resp.json(), separators=[',',':']))

    local_books = []
    for book_header in shelf['books']:
        book = { 'id': book_header['id'], 'name': book_header['name'], 'export_url': f'{BOOKS_URL}/{book_header["id"]}/export/{config.EXPORT_TYPE}' }
        local_books.append(book)
    books[shelf_header['name']] = local_books

# Print info

shelf_no = 0
book_no = 0
for shelf_name in books:
    shelf = books[shelf_name]
    shelf_no += 1
    print(f' Shelf "{shelf_name}": Found {len(shelf)} book(s)')
    book_no += len(shelf)

print(f'Found {shelf_no} shelves with {book_no} books total')

# Export

if not os.path.isdir(config.EXPORT_ROOT):
    print(f'Export root {config.EXPORT_ROOT} is not a valid path, aborting')
    exit()

backup_name = f'Export {datetime.now().strftime("%d.%m.%Y %H-%M-%S")}'
backup_dir = os.path.join(config.EXPORT_ROOT, backup_name)
os.mkdir(backup_dir)

print(f'Exporting to "{backup_dir}" as {config.EXPORT_TYPE.upper()}...')

shelf_cnt = 0
book_cnt = 0
for shelf_name in books:
    shelf = books[shelf_name]
    shelf_cnt += 1
    curr_dir = os.path.join(backup_dir, shelf_name)
    os.mkdir(curr_dir)
    local_book_cnt = 0
    for book in shelf:
        local_book_cnt += 1
        book_cnt += 1
        print(f' Exporting book {book_cnt}/{book_no}: shelf {shelf_cnt}/{shelf_no} book {local_book_cnt}/{len(shelf)} -- {book["name"]}')
        book_content_resp = requests.get(book['export_url'], headers=HEADER)
        export_file_name = f'{book["name"]}.{(config.EXPORT_TYPE if config.EXPORT_TYPE != "plaintext" else "txt")}'
        with open(os.path.join(curr_dir, export_file_name), "wb+") as file:
            file.write(book_content_resp.content)

print('Export done')
