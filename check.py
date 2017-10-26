import argparse
import sys
import multiprocessing as mp

CORES=12
test=[]
tm="" 

def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    # \b backspace
    print('\b' * width + msg, end='')
    sys.stdout.flush()


def split_file(path):
    with open(path, 'r') as ff:
        sents = ff.readlines()
    size_tst = len(sents)
    divided = size_tst / CORES
    decimal = divided - int(divided)

    divided_data = [sents[i: i + int(divided)] for i in range(0, size_tst, int(divided))]
    if decimal:
        divided_data[CORES - 1] += divided_data[CORES]
        divided_data.pop(CORES)
    assert(sum(map(lambda x: len(x), divided_data)) == size_tst)
    return divided_data

def f(part, srcD, num, queue, lock):
    total = len(part)
    count = 0
    tst = []
    ref = []
    src = []
    for i,s in enumerate(part):
        if s.strip() in tstD_set:
            count += 1	
            tst.append(s)
        else:
            ref.append(s)
            src.append(srcD[i])
        #progress('{:2.2f}% '.format((i+1) / total * 100))
    lock.wait()
    queue.put((num, src, ref, tst, count))
    print(str(num), "-number of overlapping:", count)
    lock.wait()

def paralellize(refD, srcD):
    q = mp.Queue()
    lock = mp.Barrier(CORES)
    for i, part in enumerate(refD):
        mp.Process(target=f, args=(part, srcD[i], i, q, lock)).start()

    unsorted_data = []
    for i in range(CORES):
        got = q.get()
        unsorted_data.append(got)

    return sorted(unsorted_data, key=lambda p: p[0])
"""
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
    tm = args.root[0] + '/' + args.master[0]
    test = list(map(lambda f: args.root[0] + '/' + f, args.file))
    with open(tm + '.' + tg, 'r') as ff:
        tstD = ff.readlines()

    tstD_set = set(map(lambda line: line.strip(), tstD))
    refD = split_file(test[0] + '.' + tg)
    srcD = split_file(test[0] + '.' + sl)
    sorted_data = paralellize(refD, srcD)
    ref= open("1-cleanP." + tg, 'w+') 
    src= open("1-cleanP." + sl, 'w+')
    tst= open("1-checkfileP." + tg, 'w+')
    counter_over = 0
    for i, s, r, t, c in sorted_data:
        ref.write(''.join(r))
        src.write(''.join(s))
        tst.write(''.join(t))
        counter_over += c
    ref.close()
    src.close()
    tst.close()
    print("total overlapped:", counter_over)
"""


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
