import fileinput
import argparse
import xml.etree.ElementTree as ET
import os
import sys

def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    # \b backspace
    print('\b' * width + msg, end='')
    sys.stdout.flush()

class handle_files:
    """
    A class to handle files.
    root -- working directory
    files -- files to work. If you want to parse xml, just one.
    typeT -- type of data (train, test, tuning)
    sc -- source language
    tl -- target language
    """
    def __init__(self, root, files, sc, tl, typeT=''):
        self.root = root
        self.files = files
        self.typeT = typeT
        self.sc = sc
        self.tl = tl

    def split_files(self):
        src_files = map(lambda x: self.root + '/' + x, filter(lambda file: '_' + self.sc + '.txt' in file , self.files))
        trg_files = map(lambda x: self.root + '/' + x, filter(lambda file: '_' + self.tl + '.txt' in file , self.files))

        base_filename = self.root + '/' + self.typeT
        src_filename = base_filename + '.' + self.sc + '.txt'
        trg_filename = base_filename + '.' + self.tl + '.txt'

        self.group_files(src_filename, src_files)
        self.group_files(trg_filename, trg_files)

    def group_files(self, filename, files):
        with open(filename, 'w') as f_write:
            with fileinput.input(files=files, mode='r') as f:
                for line in f:
                    f_write.write(line)
                    if line=='':
                        f_write.write('\n')

    def parse_xml(self):
        """
        Parse big xmls. Should fix partial_size / total_size
        """
        total_size = os.path.getsize(self.files[0])
        partial_size = 0
        file_sc = 'train_xml.' + self.sc + '.txt'
        file_tg = 'train_xml.' + self.tl + '.txt'
        is_source = True
        with open(file_sc, 'w') as fw_source:
            with open(file_tg, 'w') as fw_target:
                with open(self.files[0]) as f_xml: 
                    for line in f_xml:
                        partial_size += len(line)
                        line_striped = line.strip()
                        if line_striped.startswith('<seg>'):
                            if is_source:
                                fw_source.write(line_striped[5:-6])
                                fw_source.write('\n')
                            else:
                                fw_target.write(line_striped[5:-6])
                                fw_target.write('\n')
                            is_source = not is_source
                            progress('{:2.2f}% '.format((partial_size / total_size) * 100))

    def csv2file(self):
        """
        csv to plain text
        """
        base_file = self.root + '/' + 'csv2file'
        tg_file = base_file + '_' + self.tl 
        sc_file = base_file + '_' + self.sc
        with fileinput.input(files=self.files, mode='rb') as f_read:
            with open(file=sc_file, mode='wb') as fs_write:
                with open(file=tg_file, mode='wb') as fg_write:
                    for line in f_read:
                        line_splited = line.split(b';', 1)
                        fs_write.write(line_splited[0])
                        fs_write.write(b'\n')
                        fg_write.write(line_splited[1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get a set of bytecode files \
                                     and get a new one (with format UTF-16).')
    parser.add_argument('-r', '--root', help='root directory', nargs=1,
                        required=True)
    parser.add_argument('-t', '--typet', help='training or tuning', nargs=1)
    parser.add_argument('-f','--files',
                        help='list of files. Example: file1.txt file2.txt',
                        nargs='*', required=True)
    parser.add_argument('-sl', '--src_language', help='language src',
                        nargs=1, type=str, required=True)
    parser.add_argument('-tl', '--trg_language', help='language trg',
                        nargs=1, type=str, required=True)
    args = parser.parse_args()

    hf = handle_files(args.root[0], args.files, args.src_language[0], args.trg_language[0], args.typet[0])
    hf.split_files() # group all files in one.
  #  hf = handle_files(args.root[0], args.files, args.src_language[0], args.trg_language[0])
    # hf.parse_xml()
   # hf.csv2file()
