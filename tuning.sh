usage="$(basename "$0") SL TL root project_name name_file -- program to tunning a model\n\n
where:\n
      SL -- SOURCE LANGUAGUE\n
      TL -- TARGET LANGUAGUE\n
      root -- work_directory (path where you are working)\n
      project_name -- project name (a directory to put your model)\n
      name_file -- name file of your tunning file\n"

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

if [ ! -d $path_save ]; then
    echo $path_save "doesn't exist :p."
    exit
fi

# path_save into project_name
path_save=$path_save/$project_name

# tuning directory
tuning_dir=$path_save'/tuning_data'

if [ ! -d $tuning_dir ]; then
    echo 'please create a directory tuning_data in' $path_save
    exit
fi

count_dir="$(ls -l $tuning_dir | wc -l)"
if [[ $count_dir > 1 ]]; then
    echo 'Please choose one dir to work'
    all_dir="$(ls -l $tuning_dir | awk '{ print $9}')"
    echo -e $all_dir'\n'
    actual_dir=""
    read actual_dir
    tuning_dir=$tuning_dir/$actual_dir
    if [ ! -d $tuning_dir ]; then
        echo $actual_dir 'does not exist'
        exit
    fi
fi

echo $tuning_dir
read -p "wait please"
############################## TOKEN #####################################
token_dir=$tuning_dir'/token'
if [ ! -d $token_dir ]; then
    mkdir $token_dir
    read -p "token dir have just created"
fi

name_file_tuning_S=$name_file'_'$SL'.align'
name_file_tuning_T=$name_file'_'$TL'.align'
name_file_tok=$name_file'.tok'

perl $path_execute/scripts/tokenizer/tokenizer.perl -l $SL < $tuning_dir/$name_file_tuning_S > $token_dir/$name_file_tok'.'$SL
perl $path_execute/scripts/tokenizer/tokenizer.perl -l $TL < $tuning_dir/$name_file_tuning_T > $token_dir/$name_file_tok'.'$TL

read -p "tokening have already finished..."

############################# TUNINNG ################################
# nocase for case insensitive
work_dir=$path_save/working/mert-work-$name_file
if [ ! -d $work_dir ]; then
    mkdir $work_dir
fi

nohup perl $path_execute/scripts/training/mert-moses.pl $token_dir/$name_file_tok'.'$SL $token_dir/$name_file_tok'.'$TL $path_execute/bin/moses $path_save/working/model/moses.ini --mertdir $path_execute/bin/ --working-dir $work_dir --nocase  &> $work_dir/mert-out.out &
