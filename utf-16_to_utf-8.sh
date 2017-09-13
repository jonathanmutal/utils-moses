usage="$(basename "$0") PATH FORMAT -- program to convert utf-18 to utf-8\n\n
where:\n
      PATH -- Working path\n
      format -- Extension of file (ex: txt for file.txt)\n"

# arguments are correct
if [ $# -ne 2 ]; then
    echo -e $usage
    exit
fi

PATH_=$1
# format
FORMAT=$2
for d in $PATH_/*'.'$FORMAT; do
    iconv -f utf-16 -t utf-8 $d > ${d::-6}.txt
done

for d in $PATH_/*.align; do
    rm $d
done
