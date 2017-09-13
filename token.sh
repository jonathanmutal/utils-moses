
usage="$(basename "$0") root type -- program to token\n\n
where:\n
      root -- work_directory (path where you are working)\n
      type -- extension file (ex: txt for file.txt)\n"

# arguments are correct
if [ $# -ne 2 ]; then
    echo -e $usage
    exit
fi

path_execute="/home/estrella/moses/mosesdecoder"
# path where files are in.
PATH_=$1
# type file
TYPE=$2

token_dir=$PATH_'/token'
# make directory token
if [ ! -d $token_dir ]; then
    mkdir $token_dir
fi

type_len="$(expr ${#TYPE} + 1)"
for d in $PATH_/*.$TYPE; do
    echo $type_len
    L=${d::(-$type_len)}
    L=${L:(-2)}
    basefile="$(basename $d)"
    echo $L
    echo $basefile
    read -p 'wait..please'
    perl $path_execute/scripts/tokenizer/tokenizer.perl -l $L < $d > $token_dir/${basefile::(-$type_len)}'.tok'
done

