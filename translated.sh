
usage="$(basename "$0") SL path_save project_name translated_dir -- program to translated\n\n
where:\n
      SL -- SOURCE LANGUAGUE\n
      path_save -- root \n
      project_name -- project name (a directory to put your model)\n
      translated_dir -- where files are going to save."

# arguments are correct
if [ $# -ne 4 ]; then
   echo -e $usage
   exit
fi

path_execute="/home/estrella/moses/mosesdecoder"

# source language.
SL=$1
# path where files are in.
path_save=$2
# project name
project_name=$3
#where save translated files
translated_dir=$4

work_dir=$path_save/test_data/token
wk_dir=$path_save/$project_name/working
saving_dir=$path_save/$project_name/$translated_dir
for d in $work_dir/*_$SL'.'tok; do 
    basefile="$(basename $d)"
    base=${basefile:9}
    # type_train will be {mixed, PV, GB, PV}
    type_train=${base%%_*}
    nohup $path_execute/bin/moses -f $wk_dir/mert-work-Tuning_$type_train/moses.ini < $d > $saving_dir/$type_train'.'translated 2> $saving_dir/$type_train'.'out & wait $!
    
done

# for d in *_$SL'.'tok; do nohup $path_execute/bin/moses -f $project_name/mert-work-/moses.ini < $i > tuning/${i::(-4)}.tuning.translated 2> tuning/${i:0:2}.tuning.out & wait $! ; done
