from weights_config import weight_profiles, default_profile

# Choose a profile (or let user select via input/CLI/argparse)
profile = weight_profiles[default_profile]

POINT_DIFF_WEIGHT = profile["POINT_DIFF_WEIGHT"]
lead_changes_weight = profile["lead_changes_weight"]
comback_weight = profile["comeback_weight"]
OTHER_WEIGHT = 1.0 - POINT_DIFF_WEIGHT - lead_changes_weight - comback_weight  

def calculate_game_score(row):
    point_diff = abs(row['PTS_HOME'] - row['PTS_AWAY'])
    score_part = 100 if row['OT'] or point_diff == 1 else max(100 - 2 * point_diff, 0)

    comeback_part = {4: 100, 3: 90, 2: 75, 1: 60}.get(row['COMEBACK_QTR'], 50)
    lc_ties_part = min((row['LEAD_CHANGES'] + row['TIES']) * 4, 100)
    ast_part = min((row['AST_HOME'] + row['AST_AWAY']) / 50 * 100, 100)
    stl_part = min((row['STL_HOME'] + row['STL_AWAY']) / 20 * 100, 100)
    blk_part = min((row['BLK_HOME'] + row['BLK_AWAY']) / 13 * 100, 100)
    clutch_part = min(40 + row['CLUTCH_COUNT'] * 10, 100)

    other_parts = [ast_part, stl_part, blk_part, clutch_part]
    weighted_score = round(comback_weight * comeback_part + POINT_DIFF_WEIGHT * score_part + lc_ties_part * lead_changes_weight + (OTHER_WEIGHT / len(other_parts)) * sum(other_parts), 2)
    return weighted_score