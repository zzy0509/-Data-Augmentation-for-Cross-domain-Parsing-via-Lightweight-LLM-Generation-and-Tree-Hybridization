python_script="hybrid/hybrid.py"

new_dir="ewt/email/hybrid_data/temp1_ptb"
raw_data="ewt/email/hybrid_data/temp1/data_all_digit_ptb.pid"
add_data="ewt/email/hybrid_data/temp1/data_all_digit_ptb.pid"

mkdir -p ${new_dir}


n=5
i=1

while [ $i -le $n ]
do
    # echo "execute ${i} times"
    python $python_script \
        --mode random_deep \
        --input $raw_data \
        --add $add_data \
        --output "${new_dir}/tmp${i}" 
        > /dev/null 2>&1
    let i=i+1
done


final_file="${new_dir}/data_all.pid"
touch $final_file


# # # # merge
n=5
i=1
while [ $i -le $n ]
do
    # echo $i
    cat "${new_dir}/tmp${i}" >> $final_file
    let i=i+1
done

remove hiearchy
python hybrid/strip_h.py --input $final_file --output "$final_file.tmp"
rm $final_file
mv "${final_file}.tmp" $final_file

# delete repeat data
python hybrid/delete_repeat.py -i $final_file -o "${final_file}.tmp"
rm $final_file
mv "${final_file}.tmp" $final_file
