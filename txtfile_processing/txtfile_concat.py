import csv
import glob
import os
import re
from pathlib import Path

# Recursively creates list of all txt files in path directory and sub-folders in D:/
txt_paths = [str(x) for x in Path(r'D:/').glob('**/*.txt')]

# Creates list of wav-file names (regex groups before/after second .)
# Ex: 12.6474.256.3222 --> 12.6474
txt_names = [re.sub("(^[^.]+[.][^.]+)(.+$)", "\\1", os.path.basename(x))+'.wav' for x in txt_paths]

# Creates list of recording location
location_names = [x.split('.')[2] for x in txt_paths]

# Creates list of dates
dates = [os.path.basename(x)[0:10] for x in txt_paths]


out_path = r"D:\concatenated.csv"

with open(out_path, 'w', newline='') as new_file:

    csv_write = csv.writer(new_file, delimiter=',')

    for index, (file_path, file_name, location, date) in enumerate(zip(txt_paths, txt_names, location_names, dates)):
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')

            # Add new columns to header
            if index == 0:
                csv_write.writerow(next(csv_reader) + ['Length'] + ['Location'] + ['Date'] + ['File'])

            try:
                for line in csv_reader:

                    # Skip headers after the first file
                    if line[0] == 'Selection' and index != 0:
                        continue

                    else:
                        try:
                            line.extend([float(line[4])-float(line[3]), location, date, file_name])
                        except:
                            print("ERROR ADDING COLUMNS: PROBLEM WITH " + file_path)

                    # Swap Auditor and Class column for SG auditor
                    if line[7] == 'SG':
                        line[7], line[8] = line[8], line[7]

                    csv_write.writerow(line)

            except:
                print("ERROR WITH ENCODING: PROBLEM WITH " + file_path)


# Previously Used: Create list of all text files in ONLY path directory (not sub-folders)
#path = r"D:\"
#txt_paths = glob.glob(path + "/*.txt")