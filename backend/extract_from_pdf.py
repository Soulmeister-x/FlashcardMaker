import logging
import sys
import pymupdf
from dotenv import load_dotenv


logger = logging.getLogger('extract_pdf')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s  - %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
fh = logging.FileHandler('extraction.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)

load_dotenv()

file_name = os.environ.get('PDF_FILE')
pdf_file = pymupdf.open(file_name)
pdf_file.authenticate(os.environ.get('PDF_PASSWORD'))

# read labels, which are lines in the pdf that should get skipped
labels = []
with open('labels.txt') as label_file:
    labels = [label for label in label_file.readlines()]

logger.info(f"{pdf_file.page_count} pages in {file_name}")
logger.info("labels that should get skipped:")
for label in labels:
    logger.info(label)

for page in pdf_file.pages():
    cur_page = page.get_text()
    logger.info(cur_page)
    # if 'q' == input():
    #    break


with open('extraction.log') as ex_log:
    lines = ex_log.readlines()

with open('extraction-filtered.log', 'w') as ex_log:
    for line in lines:
        if line.strip("\n") not in labels:
            ex_log.write(line)
