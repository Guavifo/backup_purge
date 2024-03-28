# -*- coding: utf-8 -*-
"""
Program to efficiently purge backup drives

TODO: Add a GUI
TODO: Write the start end end times to a text file that can be referenced later
TODO: Write any errors to a log file
TODO: Update the user with how many unique files have been found as the 
        program runs, not just at the end (in case of failure)
TODO: Play with the buffer size and see if that speeds things up
TODO: Remove the universal file name when writing to the CSV file
TODO: Add error checking for the hashing function so that skips 
        files that can't be accessed instead of the whole program failing
TODO: Make this multithreaded so that it pulls from two sources at once

"""

import os
# import sys
import hashlib
import openpyxl
import time

print()
print("This program will tell you which files on your backup drive")
print("are *not* present in your archive drive. The files which are")
print("unique to your backup drive will be saved in an text file.")
print()
print("This program does not support network locations, please map")
print("any drives to a local drive letter first.")
print()
archive_name = input("Please enter the full path of your archive drive: ")
backup_name = input("Please enter the full path of your backup drive: ")


archive_name = '\\\\?\\' + archive_name
backup_name = '\\\\?\\' + backup_name

print(archive_name)
print(backup_name)

# Set a timer to see how long this takes
start_time = time.time()

print()
print("Looking through the archive drive now...")
archive = []
count = 0
total_size = 0

for root, dirs, files in os.walk(archive_name):
   for name in files:
      # print(os.path.join(root, name))
      file_size = os.path.getsize(os.path.join(root, name))
      archive.append([root, name, file_size])
      total_size = total_size + file_size
      count = count + 1
      if count % 1000 == 0:
          print(f'{count:,} files found in the archive so far')
   # for name in dirs:
      # print(os.path.join(root, name))

print()
print('In archive location:', archive_name)
print(f'{count:,} files found in the archive in total')
print(f'{total_size:,} bytes used in the archive in total')

print()
print("Looking through the backup drive now...")
backup = []
count = 0
total_size = 0

for root, dirs, files in os.walk(backup_name):
   for name in files:
      # print(os.path.join(root, name))
      file_size = os.path.getsize(os.path.join(root, name))
      backup.append([root, name, file_size])
      total_size = total_size + file_size
      count = count + 1
      if count % 1000 == 0:
          print(f'{count:,} files found in the backup so far')
   # for name in dirs:
      # print(os.path.join(root, name))
      
print()
print('In backup location:', backup_name)
print(f'{count:,} files found in the backup in total')
print(f'{total_size:,} bytes used in the backup in total')
print()


# Find the unique files in the backup drive
unique = []


BUF_SIZE = 65536 
files_checked = 0


for b_file in backup:
    files_checked = files_checked + 1
    if files_checked % 100 == 0:
        percent = files_checked / count
        print(f'{files_checked:,} files hashed in the backup so far ({percent:.2%})')
    match = False
    b_root, b_name, b_size = b_file
    # print(root, name, f'{size:,}')
    for a_file in archive:
        a_root, a_name, a_size = a_file
        
        # Check if the filename and the size match before hashing the file
        if b_name == a_name and b_size == a_size:
            
            # Generate the hash for the Archive file
            a_md5 = hashlib.md5()
            with open(os.path.join(a_root, a_name), 'rb') as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    a_md5.update(data)
            # print("A_MD5: {0}".format(a_md5.hexdigest()))
            
            # Generate the hash for the Backup file
            b_md5 = hashlib.md5()
            with open(os.path.join(b_root, b_name), 'rb') as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    b_md5.update(data)
            # print("B_MD5: {0}".format(b_md5.hexdigest()))           
            
            # If the hashes match, this is a confirmed duplicate file
            if a_md5.hexdigest() == b_md5.hexdigest():
                match = True
                break
            
    if match == False:
        unique.append(b_file)

if len(unique) == 0:
    print("There were no unique files on the backup drive")
else:
    print('Below are the unique files:')
    with open('unique.txt', 'w') as f:
        for u_file in unique:
            print(u_file)
            for item in u_file:
                # write each item on a new line
                f.write("%s\n" % item)
    print('These are also saved to unique.txt')
    
    # create a new workbook
    workbook = openpyxl.Workbook()

    # select the active worksheet
    worksheet = workbook.active
    worksheet.append(['File Path', 'Name', 'Size'])

    # loop through the list of lists and write each row to the worksheet
    for row in unique:
        formatted_row = [str(cell) if i != 2 else '{:,.0f}'.format(cell) for i, cell in enumerate(row)]
        worksheet.append(formatted_row)

    # save the workbook
    workbook.save("unique_files.xlsx")

# check the timer again
end_time = time.time()
total_time = end_time - start_time
print(f'Total time: {total_time:.2f} seconds')

print('Done!')

# End of program
