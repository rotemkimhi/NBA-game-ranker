from nba_api.stats.endpoints import playbyplayv2

COMEBACK_THRESHOLD = 15  # Points

def detect_comeback_quarter(game_id, threshold=15):
    try:
        pbp = playbyplayv2.PlayByPlayV2(game_id=game_id)
        df = pbp.get_data_frames()[0]

        comeback_quarter = None
        home_trailed_by = away_trailed_by = 0
        comeback_triggered_home = comeback_triggered_away = False

        for _, row in df.iterrows():
            if isinstance(row.get("SCORE"), str) and "-" in row["SCORE"]:
                try:
                    away_score, home_score = map(int, row["SCORE"].split("-"))
                    quarter = row["PERIOD"]
                    diff = home_score - away_score

                    if diff > 0:
                        away_trailed_by = max(away_trailed_by, diff)
                    elif diff < 0:
                        home_trailed_by = max(home_trailed_by, abs(diff))

                    if (away_trailed_by >= threshold and diff <= 0 and not comeback_triggered_away):
                        comeback_quarter = quarter
                        comeback_triggered_away = True

                    if (home_trailed_by >= threshold and diff >= 0 and not comeback_triggered_home):
                        comeback_quarter = quarter
                        comeback_triggered_home = True

                except:
                    continue
        return comeback_quarter
    except Exception as e:
        print(f"Error detecting comeback quarter for {game_id}: {e}")
        return None