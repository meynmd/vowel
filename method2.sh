#!/bin/bash

python3 word_char.py corpus_v2 > corpus_word_char_model_v2
python3 char_word.py corpus_v2 > corpus_char_word_model_v2
python3 bigram.py corpus_v2 > corpus_bigram_model_v2
./carmel_mac corpus_char_word_model_v2 corpus_bigram_model_v2 corpus_word_char_model_v2 remove-vowels.fst > all_combined_model
cat strings.novowels | ./carmel_mac -sribIEWk 1 all_combined_model > re_vowels
python eval.py strings re_vowels
