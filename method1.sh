python make.py > english_vocab_method1.fsa
python building_model.py > character_fst_method1
./carmel_mac english_vocab_method1.fsa character_fst_method1 remove-vowels.fst > first_combined_fst_method1
cat strings.novowels | ./carmel_mac -sribIEWk 1 first_combined_fst_method1 > string_restore_method1
python eval.py strings string_restore_method1

