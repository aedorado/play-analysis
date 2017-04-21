for entry in "lemma_cat_folder/"*
do
	echo "Processing $entry"
	./a.out $entry
done