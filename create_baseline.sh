path_execute="/home/estrella/moses/mosesdecoder"
# pource language.
SL=$1
# target language.
TL=$2
# path where files are in.
path_save=$3
# project name
project_name=$4

# names' files
name_file='train'
if [ ! -d $path_save ]; then
    echo $path_save "doesn't exist :p."
    exit
fi

# path_save into project_name
path_save=$path_save/$project_name

if [ ! -d $path_save ]; then
    echo $project_name"doesn't exist. Also remeber that you need to make a train_data directory"
fi
# train directroy
train_dir=$path_save'/train_data'

if [ ! -d $train_dir ]; then
    echo 'please create a directory train_data in' $path_save
    exit
fi

############################# TOKENIZATOR ###################################
token_dir=$path_save'/token'
# make directory token
if [ ! -d $token_dir ]; then
    mkdir $token_dir
fi

name_file_train_S=$name_file'.'$SL'.'txt
name_file_train_T=$name_file'.'$TL'.'txt

if [ ! -f $train_dir/$name_file_train_T ]; then
    read -p "The training data is getting ready, press enter!"
    python3 ~/moses/jonhy_ws/scripts/split_data.py -r $train_dir -t $name_file -f *'.align' -sl $SL -tl $TL
fi

name_file_tok=$name_file'.tok'
perl $path_execute/scripts/tokenizer/tokenizer.perl -l $SL < $train_dir/$name_file_train_S > $token_dir/$name_file_tok'.'$SL
perl $path_execute/scripts/tokenizer/tokenizer.perl -l $TL < $train_dir/$name_file_train_T > $token_dir/$name_file_tok'.'$TL

echo "tokening have already finished..."
############################# CLEAN DATA #####################################
opt=''
while [[ $opt != 'Y' && $opt != 'N' ]] ; do
    echo 'Clean data?[Y/N]'
    read opt
done

if [[ $opt == 'Y' ]]; then
    name_file_clean=$name_file'.clean'
    perl $path_execute/scripts/training/clean-corpus-n.perl $token_dir/$name_file_tok $SL $TL $token_dir/$name_file_clean 1 90
    echo 'Data cleaned'
else
    name_file_clean=$name_file_tok
fi

############################# MODEL LANGUAGE ###################################
# to make directory for model language
ml_dir=$path_save'/ml'
if [ ! -d $ml_dir ]; then
    mkdir $ml_dir
fi

echo "It's time to train our Model Language!"
echo "We are working in this, please be pacient! For now we only train n-grams models"

n_gram=-1
while [ $n_gram -lt 0 ]; do
    echo 'Please choose an N for N-gram'
    read n_gram
done

# build our n-gram model
model_file=$name_file'.arpa.'$TL
$path_execute/bin/lmplz -o $n_gram < $token_dir/$name_file_clean'.'$TL > $ml_dir/$model_file

# binarise our lenguage model
binarise_file=$name_file'.blm.'$TL
$path_execute/bin/build_binary $ml_dir/$model_file $ml_dir/$binarise_file

echo "modeling have already finished..."
########################### TRANSLATION SYSTEM #################################
echo "Finally we come to the main event! You are doing the things well!"

# make directory for translation system
trans_dir=$path_save'/working'
if [ ! -d $trans_dir ]; then
    mkdir $trans_dir
fi

nohup perl $path_execute/scripts/training/train-model.perl -root-dir $trans_dir -corpus $token_dir/$name_file_clean -f $SL -e $TL -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0':'3':'$ml_dir/$binarise_file':'8 -external-bin-dir $path_execute/tools >& $path_save/training.out &
