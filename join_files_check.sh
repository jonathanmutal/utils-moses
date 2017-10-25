for d in *_de.txt; do wc -l $d; done | awk '{print $1}' | paste -sd+ | bc
