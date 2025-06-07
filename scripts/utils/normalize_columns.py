# scripts/utils/normalize_columns.py

import pandas as pd

RENAME_COLS = {
    "prob_1": "implied_prob_1",
    "prob_2": "implied_prob_2",
    "margin": "odds_margin",
    "prob_diff": "implied_diff",
    "odds1": "odds_player_1",
    "odds2": "odds_player_2",
}

REQUIRED_COLS = [
    "market_id", "player_1", "player_2", "odds_player_1", "odds_player_2",
    "match_id", "actual_winner", "winner_name", "loser_name",
    "match_date", "selection_id_1", "selection_id_2"
]


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = df.rename(columns=RENAME_COLS)

    if "odds" not in renamed.columns and "odds_player_2" in renamed.columns:
        renamed["odds"] = renamed["odds_player_2"]
    if "odds_2" not in renamed.columns and "odds_player_1" in renamed.columns:
        renamed["odds_2"] = renamed["odds_player_1"]

    if "implied_prob" not in renamed.columns and "odds" in renamed.columns:
        renamed["implied_prob"] = 1 / renamed["odds"]
    if "implied_prob_2" not in renamed.columns and "odds_player_2" in renamed.columns:
        renamed["implied_prob_2"] = 1 / renamed["odds_player_2"]
    if "implied_prob_1" not in renamed.columns and "implied_prob_2" in renamed.columns:
        renamed["implied_prob_1"] = 1 - renamed["implied_prob_2"]
    if "implied_diff" not in renamed.columns and "implied_prob_1" in renamed.columns and "implied_prob_2" in renamed.columns:
        renamed["implied_diff"] = renamed["implied_prob_1"] - renamed["implied_prob_2"]

    missing = [col for col in REQUIRED_COLS if col not in renamed.columns]
    if missing:
        raise ValueError(f"❌ Missing required columns: {missing}. Available: {list(renamed.columns)}")

    return renamed


def patch_winner_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds or fixes the 'winner' column based on actual_winner vs player_1.
    """
    if "winner" not in df.columns:
        if "actual_winner" in df.columns and "player_1" in df.columns:
            df["winner"] = (
                df["actual_winner"].str.strip().str.lower() ==
                df["player_1"].str.strip().str.lower()
            ).astype(int)
    return df
