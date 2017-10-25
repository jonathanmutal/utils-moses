usage="$(basename "$0") root type SL TL -- program to token\n\n
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
for d in $PATH_/*'.'$TYPE; do
    L=${d::(-$type_len)}
    L=${L:(-2)}
    basefile="$(basename $d)"
    basefile="${basefile::(-$type_len)}"
    basefile="${basefile::(-3)}"
    echo $L
    echo $basefile
    echo $d
    read -p 'wait..please'
    perl $path_execute/scripts/tokenizer/tokenizer.perl -l $L -threads 12 < $d > $token_dir/$basefile'.'tok.$L
done

