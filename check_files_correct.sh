ROOT=$1
FILE=$2
L=${FILE:(-2)}
echo $L
FILE=$ROOT/$FILE
count_line=1
for d in $ROOT/*'.'$L; do
    echo $d
    echo $FILE
    read -p 'wait4'
    if  [ "$FILE" == "$d" ]; then
         echo $d
         continue
    fi
    s2="$(awk 'FNR==1' $d)"
    s1="$(awk 'FNR=='$count_line $FILE)"

    echo $s1
    echo $s2
    read -p 'waiit3'
    lines="$(wc -l $d | awk '{ print $1 }')"
    let count_line="$(expr $count_line + $lines)"
done
