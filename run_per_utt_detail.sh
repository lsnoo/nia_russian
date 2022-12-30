. ../path.sh

#wer_scoring
compute-wer ark:ref ark:hyp > wer_results


#align-text ark:ref ark:hyp ark,t:- |
#	../utils/scoring/wer_per_utt_details.pl > per_utt_results

align-text --special-symbol='**' ark:ref ark:hyp ark,t:- |
	../utils/scoring/wer_per_utt_details.pl --special-symbol='**' > per_utt_results

#align-text --special-symbol=â**â ark:ref_jamo_phn_to_jamo ark:hyp_jamo_phn_to_jamo ark,t:- | ../utils/scoring/wer_per_utt_details.pl --special-symbol â**â > per_utt_results_jamo_phn_to_jamo

