# download citations from the Open Citation Index

# Download source page:
# https://figshare.com/articles/Crossref_Open_Citation_Index_CSV_dataset_of_all_the_citation_data/6741422/3

export DOWNLOAD_URL="https://ndownloader.figshare.com/articles/6741422/versions/9"
export DESTINATION_FILE="./data/citation_data.zip"
export DESTINATION_FOLDER="./data"

rm -f $DESTINATION_FILE

wget -q -N $DOWNLOAD_URL -O $DESTINATION_FILE

unzip -o $DESTINATION_FILE -d $DESTINATION_FOLDER/

for x in $DESTINATION_FOLDER/20*.zip ; do unzip -d $DESTINATION_FOLDER/all -o -u $x ; done

cat $DESTINATION_FOLDER/all/*.csv > $DESTINATION_FOLDER/data.csv
