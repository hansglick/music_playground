# SELECTION DES TRACKS A TELECHARGER
JSONFILE=$1
jq '.[0:6]' < $JSONFILE | jq '.[] .youtube[] .id' > someids.txt
filename="someids.txt"



# RECENSE LES TRACKS DEJA TELECHARGES
files_array=()
ls >> temp_files
while read line

do

x=$(basename $line)
files_array+=($x)

done < temp_files



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

done < $filename



# REMOVE USELESS TEMP FILES
rm $filename
rm "temp_files"