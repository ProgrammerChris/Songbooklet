from PyPDF2 import PdfFileMerger, PdfFileReader
import os
from app import app
import json


""" Merge given PDFs to one file with a given filename.

    Contains one method, merge_pdfs(dict).
    
    modules:
        os
        app(to get the app root in the flask app)
        PyPDF2 - PdfFileMerger and PdfFileReader

"""


def merge_pdfs(songs):
    """Merge a given dict of PDFs to a singe PDF, and give the file a name given from the 'filename' key in the dict.
    argument:
        songs -- a dict containing keys of artist and song ie: key: 'brucespringsteenkingdomofdays',
                                                            value: '[bruce springsteen, kingdom of days]'
                 should also contain a key of 'filename' with a value of the wanted name of the merged file.

    """
    # Initialize list to populate with songs choosen by user and later create booklet.
    pdfs = []

    # Path to PDFs
    pdf_dir = '/home/chris/pdfs/' #app.root_path + '/static/pdfs/'

    # Path to final booklet
    booklets_dir = app.root_path + '/static/booklets/'

    # Getting filename from dict to be used for the final merged file, if no filename, use booklet as default.
    filename = songs['filename'] if songs['filename'] else 'booklet'

    available_pdfs = sorted(os.listdir(pdf_dir))
    songs_to_merge = json.loads(songs['songs']).values()
    '''
    for song in songs_to_merge:
        song_pdf = song[0].lower() + ' - ' + song[1].lower() + '.pdf'
        if song_pdf in available_pdfs:
           pdfs.append(pdf_dir + song_pdf)

    '''
    # binarysearch the directory of PDFs to find each PDF to be merged
    for song in songs_to_merge:
        song_pdf = song[0].lower() + ' - ' + song[1].lower() + '.pdf'
        start = 0
        end = len(available_pdfs) - 1

        while start <= end:
            middle = (start + end) // 2
            midpoint = available_pdfs[middle]

            if midpoint > song_pdf:
                end = middle - 1
            elif midpoint < song_pdf:
                start = middle + 1
            else:
                pdfs.append(pdf_dir + song_pdf)
                break

    # --- Merging pdfs to booklet ---
    merger = PdfFileMerger()

    for pdf in pdfs:
        merger.append(PdfFileReader(pdf))

    merger.write(booklets_dir + filename + '.pdf')

    return booklets_dir + filename + '.pdf'


