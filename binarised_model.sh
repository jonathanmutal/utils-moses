
usage="It's not finished because It needs some libraries!\n$(basename "$0") SL TL root project_name name_file -- binarised a model\n\n
where:\n
      SL -- SOURCE LANGUAGUE\n
      TL -- TARGET LANGUAGUE\n
      root -- work_directory (path where you are working)\n
      project_name -- project name (a directory to put your model)\n"

# arguments are correct
if [ $# -ne 5 ]; then
    echo -e $usage
    exit
fi

path_execute="/home/estrella/moses/mosesdecoder"

# source language.
SL=$1
# target language.
TL=$2
# path where files are in.
path_save=$3
# project name
project_name=$4
# file_name
name_file=$5

working_dir_bin=$path_save/working/mert-work-$name_file
if [ ! -d $work_dir_bin ]; then
    echo "$work_dir_bin doesn't exist, please train it before binarized"
    exit
fi

$path_execute/bin/procces
