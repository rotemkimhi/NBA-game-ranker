def detect_overtime(line_scores):
    score_cols = [col for col in line_scores.columns if col.startswith('PTS_')]
    ot_cols = [col for col in score_cols if 'OT' in col]
    if ot_cols:
        for col in ot_cols:
            if line_scores[col].sum() > 0:
                return True
    return False