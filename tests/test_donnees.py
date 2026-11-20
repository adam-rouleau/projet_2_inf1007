from pathlib import Path

from src.donnees import DataManager


def test_data_manager_loads_csv_and_splits_features():
    csv_path = Path(__file__).resolve().parent.parent / "movie_blockbusters.csv"
    manager = DataManager(str(csv_path))

    features, target = manager.donnees_clean

    assert list(features.columns) == ["genre", "budget_usd", "rating", "runtime_min"]
    assert len(features) == len(target)
    assert set(target.unique()).issubset({0, 1})