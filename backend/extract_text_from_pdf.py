""" Flashcard Maker
1. read pdf file
2. extract pages
3. clean pages (ML ?)
4. compress data
5. define flashcard format
6. define AI prompt
7. send request to AI
8. save response
9. split flashcards
10. separate question and answer
11. define csv format
12. print flashcard data as format
13. output as csv
(14. import to anki)
"""
import os


def read_pdf_file(file_path, file_password=None):
    import pymupdf
    reader = pymupdf.open(file_path)
    if file_password:
        reader.authenticate(file_password)

    contents = []
    for page in reader.pages():
        contents.append(page.get_text())
    return contents


def find_repeating_strings(lines):
    labels = {}

    # count all string occurances
    for line in lines:
        if line not in labels.keys():
            labels[line] = 0
        else:
            labels[line] += 1

    # get mean amount of string occurances
    total_num = sum([labels[label] for label in labels])
    mean_num = total_num / len(labels)
    repeating_labels = {}
    for label, n in labels.items():
        if n > mean_num:
            repeating_labels[label] = n

    return repeating_labels


def extract_data_from_pdf():
    file_path = 'data/in/KNN&ML24_25.pdf'
    file_path = 'data/in/KNNML_skript_vorlaeufig_24_25.pdf'
    file_password = 'knn03nmi'
    contents = read_pdf_file(file_path=file_path, file_password=file_password)
    print(f"{len(contents)} pages were extracted from {file_path}")

out_path = 'data/out/'
extracted_file_path = os.path.join(out_path, 'extracted.txt')
def write_to_file():
    with open(extracted_file_path, 'w') as f:
        for page in contents:
            f.write(page)
            f.write("----------")
    print(f"pages were written to: {out_path}")

def main():
    # remove repeating lines
    with open(extracted_file_path) as f:
        all_lines = f.readlines()  #[:100]
    
    all_lines_stripped = [line.strip() for line in all_lines]
    unique_lines = dict.fromkeys(set(all_lines))

    print(f"found {len(all_lines)}")
    print(f"unique lines {len(unique_lines)}")

    # count occurences
    for line in unique_lines:
        n = sum([1 for l in all_lines if l == line])
        unique_lines[line] = n
    
    unique_lines_filtered = {}
    for key, value in unique_lines.items():
        if value > 1:
            unique_lines_filtered[key] = value

    unique_lines_filtered = sorted(unique_lines_filtered.items(), key=lambda item: item[1], reverse=True)

    print(*unique_lines_filtered, sep="\n")

    #labels = find_repeating_strings(f.readlines())
    labels = [l[0] for l in unique_lines_filtered]
    print("\nFollowing labels will be removed:")
    print(*enumerate(labels), sep="\n")

    choice = input("Choose invalid labels (e.g. '1' '1-3' or '1,3')\n> ")
    if choice:
        choices = choice.split(',')

    # parse selected choices
    nums = set()
    for choice in choices:
        if '-' in choice:
            start, end = choice.split('-')
            for n in range(int(start), int(end)+1):
                nums.add(int(n))
        else:
            nums.add(int(choice))

    # remove labels by choice id
    nums = reversed(list(nums))
    for num in nums:
        del labels[num]

    print('will remove the following labels:')
    print(*labels, sep='\n')

    if 'n' == input('Proceed? [Y/n]: ').lower():
        exit(0)

    counter = 0
    with open(os.path.join(out_path, 'extracted_reduced.txt'), 'w') as f:
        for line in all_lines:
            if line in labels:
                print(f"skipped: '{line}'")
                continue
            counter += 1
            f.write(line)


#def main():
#    #clean_data()


if '__main__' == __name__:
    main()