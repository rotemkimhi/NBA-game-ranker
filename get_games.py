from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2, boxscoresummaryv2, playbyplayv2
import pandas as pd
import time

from overtime import detect_overtime
from clutch import count_clutch_moments
from comeback import detect_comeback_quarter
from game_score import calculate_game_score

# CONFIGURABLE PARAMS
target_date = "2025-06-11"

def fetch_games_on_date(date_str):
    all_data = []

    gamefinder = leaguegamefinder.LeagueGameFinder(league_id_nullable="00")
    df = gamefinder.get_data_frames()[0]
    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
    games = df[df['GAME_DATE'] == pd.to_datetime(date_str)]
    game_ids = games['GAME_ID'].unique()

    for game_id in game_ids:
        time.sleep(0.6)
        try:
            summary = boxscoresummaryv2.BoxScoreSummaryV2(game_id=game_id)
            summary_df = summary.get_data_frames()[1]
            line_score_df = summary.get_data_frames()[5]

            lead_changes = summary_df['LEAD_CHANGES'].values[0]
            ties = summary_df['TIMES_TIED'].values[0]
            ot = detect_overtime(line_score_df)
            clutch = count_clutch_moments(game_id)
            comeback_qtr = detect_comeback_quarter(game_id)

            team_stats = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id).get_data_frames()[1]

            if len(line_score_df) != 2:
                continue

            away_team_row = line_score_df.iloc[0]
            home_team_row = line_score_df.iloc[1]
            home_row = team_stats[team_stats['TEAM_ID'] == home_team_row['TEAM_ID']].iloc[0]
            away_row = team_stats[team_stats['TEAM_ID'] == away_team_row['TEAM_ID']].iloc[0]

            matchup = f"{home_team_row['TEAM_CITY_NAME']} vs. {away_team_row['TEAM_CITY_NAME']}"

            all_data.append({
                'GAME_ID': game_id,
                'MATCHUP': matchup,
                'PTS_HOME': home_row['PTS'],
                'PTS_AWAY': away_row['PTS'],
                'AST_HOME': home_row['AST'],
                'AST_AWAY': away_row['AST'],
                'STL_HOME': home_row['STL'],
                'STL_AWAY': away_row['STL'],
                'BLK_HOME': home_row['BLK'],
                'BLK_AWAY': away_row['BLK'],
                'OT': ot,
                'LEAD_CHANGES': lead_changes,
                'TIES': ties,
                'COMEBACK_QTR': comeback_qtr,
                'CLUTCH_COUNT': clutch,
            })

        except Exception as e:
            print(f"Error processing {game_id}: {e}")
            continue

    return pd.DataFrame(all_data)

if __name__ == "__main__":
    df = fetch_games_on_date(target_date)
    pd.set_option('display.max_columns', None)
    if df.empty:
        print(f"No games found on {target_date}.")
        exit()

    df['GAME_SCORE'] = df.apply(calculate_game_score, axis=1)
    df_sorted = df.sort_values(by='GAME_SCORE', ascending=False)

    for _, row in df_sorted.iterrows():
        print(f"{row['MATCHUP']} — Score: {row['GAME_SCORE']}")

    df_sorted.to_csv(f"nba_games_{target_date}.csv", index=False)
    print(f"Data saved to nba_games_{target_date}.csv")
