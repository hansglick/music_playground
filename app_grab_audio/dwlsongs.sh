# SELECTION DES TRACKS A TELECHARGER
JSONFILE=$1
jq '.[0:2]' < $JSONFILE | jq '.[] .youtube[] .id' > someids.txt
filename="someids.txt"
#filename=$(mktemp /tmp/someids.txt)

# RECENSE LES TRACKS DEJA TELECHARGES
#files_array=()
#for file in /home/serge/proj/adthena/pure/*
#do
# x=$(basename $file)
# #echo "$x"
# files_array+=($x)
#done



files_array=()
ls >> temp_files
while read line

do

x=$(basename $line)
#echo "$x"
files_array+=($x)

done < temp_files




#echo "${files_array[@]}"
#echo ""


# Téléchargement des mp3s, uniquement s'ils n'ont pas été dwlded
while read line; do

youtubeid="${line%\"}"
youtubeid="${youtubeid#\"}"
myurl="https://www.youtube.com/watch?v=${youtubeid}"

yid="${youtubeid}.mp3"



if [[ " ${files_array[@]} " =~ " ${yid} " ]]; then
:
else
youtube-dl -x --audio-format mp3 -o "%(id)s.%(ext)s" --audio-quality 9 $myurl
fi

#echo ""

done < $filename

rm $filename
rm "temp_files"