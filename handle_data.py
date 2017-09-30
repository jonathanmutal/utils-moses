import fileinput
import argparse
import os
import sys
import re

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
        file_sc = 'train.' + self.sc + '.txt'
        file_tg = 'train.' + self.tl + '.txt'
        is_source = True
        with open(file_sc, 'w') as fw_source:
            with open(file_tg, 'w') as fw_target:
                with open(self.files[0]) as f_xml: 
                    for line in f_xml:
                        partial_size += len(line)
                        line_striped = line.strip()
                        if line_striped.startswith('<seg>'):
                            while "</seg>" not in line_striped:
                                aline = f_xml.readline()
                                partial_size += len(aline)
                                line_striped += aline.strip()
                            line_clean = re.sub('<seg>', '', line_striped)
                            line_clean = re.sub('</seg>', '', line_clean)
                            if "<bpt" in line_clean:
                                line_clean = re.sub('<bpt.*? />', '', line_clean)
                            if "<ept" in line_clean:
                                line_clean = re.sub('<ept.*? />', ' ', line_clean)
                            if "<ph" in line_clean:
                                line_clean = re.sub('<ph.*? />', '', line_clean)
                            if is_source:
                                fw_source.write(line_clean)
                                fw_source.write('\n')
                            else:
                                fw_target.write(line_clean)
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

