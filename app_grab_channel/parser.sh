filename=$1

while read line; do

arrIN=(${line//;/ })
myurl="https://www.youtube.com/watch?v=${arrIN[1]}"
echo $myurl >> $2

done < $filename