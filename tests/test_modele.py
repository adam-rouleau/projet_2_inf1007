import pandas as pd

from src.modele import ModeleBlockbuster


def test_pipeline_accepts_clean_feature_tuple():
    features = pd.DataFrame({
        "genre": ["Action", "Comedy"],
        "budget_usd": [1000000.0, 2000000.0],
        "rating": [8.0, 6.5],
        "runtime_min": [120.0, 95.0],
    })
    target = pd.Series([1, 0])

    modele = ModeleBlockbuster((features, target))

    assert modele.pipeline is not None