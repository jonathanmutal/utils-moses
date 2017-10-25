import argparse
from handle_data import handle_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get a set of bytecode files \
                                     and get a new one (with format UTF-16).')
    parser.add_argument('-r', '--root', help='root directory', nargs=1,
                        required=True)
    parser.add_argument('-t', '--typet', help='training or tuning',
                        nargs=1, required=True)
    parser.add_argument('-f','--files',
                        help='list of files. Example: file1.txt file2.txt',
                        nargs='*', required=True)
    parser.add_argument('-sl', '--src_language', help='language src',
                        nargs=1, type=str, required=True)
    parser.add_argument('-tl', '--trg_language', help='language trg',
                        nargs=1, type=str, required=True)
    args = parser.parse_args()
#    hf = handle_files(args.root[0], args.files, args.src_language[0], args.trg_language[0], args.typet[0])
#    hf.split_files() # group all files in one.
    hf = handle_files(args.root[0], args.files[0], args.src_language[0], args.trg_language[0], args.typet[0])
    hf.parse_xml()
   # hf.csv2file()
