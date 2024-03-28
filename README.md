# Backup Purge

Backup Purge is a command-line program designed to find unique files on backup drives, helping users manage their backup data more efficiently.

## How It Works

Backup Purge works by comparing the contents of two backup drives and identifying files that are unique to each drive. It employs the following steps:

1. **Input**: The user provides the paths to the two backup drives to be compared.

2. **File Comparison**: The program recursively scans the directories on both backup drives and creates a list of files present on each drive.

3. **Comparison Analysis**: It then compares the lists of files from both drives to identify files that are unique to each drive. This is done by hashing all files which have 

4. **Output**: The program generates a report listing the unique files found on each backup drive.

## Usage

To use Backup Purge:

1. Clone or download the program files to your local machine.

2. Ensure you have Python installed on your system.

3. Open a terminal or command prompt and navigate to the directory containing the program files.

4. Run the program with the following command:
python backup_purge.py /path/to/main_or_archive/drive /path/to/backup/drive

5. Wait for the program to complete its analysis. Once finished, it will generate text files indicating the unique files found on each drive.

## Note

- This program assumes that both backup drives are accessible from the local file system, you may need to map network drive first
- Depending on the size and contents of the backup drives, the program's execution time may vary.

## License

This program is distributed under the MIT License.
