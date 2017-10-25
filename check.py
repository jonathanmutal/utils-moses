import argparse
import sys

test = []
tm = "" 

def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    # \b backspace
    print('\b' * width + msg, end='')
    sys.stdout.flush()

def check_file(sl, tg):
    for f in test:
        print(f)
        with open(f + '.' +  tg, 'r') as ff:
            refD = ff.readlines()
        with open(f + '.' + sl, 'r') as ff:
            srcD = ff.readlines()
        with open(tm + '.' + tg, 'r') as ff:
            tstD = ff.readlines()

        tstD_set = set(map(lambda line: line.strip(), tstD))

        total = len(refD)
        count = 0
        for i,s in enumerate(refD):
            if s.strip() in tstD_set:
                count += 1	
                tst.write(s)
            else:
                ref.write(s)
                src.write(srcD[refD.index(s)])
            progress('{:2.2f}% '.format((i+1) / total * 100))
        print("number of overlapping:", count)
    tst.close()
    ref.close()
    src.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Verify overlapping')
    parser.add_argument('-r', '--root', help='root directory', nargs=1,
                        required=True)
    parser.add_argument('-f','--file', help='file to check', nargs='*', required=True)
    parser.add_argument('-m','--master',
                        help='master file to check. Example: file1.txt file2.txt',
                        nargs=1, required=True)
    parser.add_argument('-sl', '--src_language', help='language src',
                        nargs=1, type=str, required=True)
    parser.add_argument('-tl', '--trg_language', help='language trg',
                        nargs=1, type=str, required=True)
    args = parser.parse_args()
    tg = args.trg_language[0]
    sl = args.src_language[0]
    ref= open("1-clean." + tg, 'w+') 
    src= open("1-clean." + sl, 'w+')
    tst= open("1-checkfile." + tg, 'w+')
    tm = args.root[0] + '/' + args.master[0]
    test = map(lambda f: args.root[0] + '/' + f, args.file)
    check_file(sl, tg)
    
