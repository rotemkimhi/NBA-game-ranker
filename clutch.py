from nba_api.stats.endpoints import playbyplayv2

def count_clutch_moments(game_id):
    try:
        pbp = playbyplayv2.PlayByPlayV2(game_id=game_id)
        df = pbp.get_data_frames()[0]

        clutch_events = 0

        def time_to_seconds(timestr):
            try:
                mins, secs = map(int, timestr.split(':'))
                return mins * 60 + secs
            except:
                return 999

        df['SECONDS'] = df['PCTIMESTRING'].apply(time_to_seconds)

        # Track score starting from last 5 minutes of 4th quarter and all OT
        track_window = df[((df['PERIOD'] == 4) & (df['SECONDS'] <= 300)) | (df['PERIOD'] > 4)]

        last_home_score = 0
        last_away_score = 0

        for _, row in track_window.iterrows():
            # Update score if possible
            score_str = row.get("SCORE")
            if isinstance(score_str, str) and '-' in score_str:
                try:
                    last_away_score, last_home_score = map(int, score_str.split('-'))
                except:
                    pass

            # Only check for clutch moments in last 2 minutes
            if row['SECONDS'] > 180:
                continue

            margin = abs(last_home_score - last_away_score)
            if margin > 5:
                continue

            msg_type = row['EVENTMSGTYPE']
            description = f"{row.get('HOMEDESCRIPTION', '')} {row.get('VISITORDESCRIPTION', '')}".lower()

            if msg_type == 1:
                clutch_events += 1
            elif msg_type == 5 and 'steal' in description:
                clutch_events += 1
            elif msg_type == 2 and 'block' in description:
                clutch_events += 1

        return clutch_events
    except Exception as e:
        print(f"Error counting clutch moments for {game_id}: {e}")
        return 0