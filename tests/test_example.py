import os
import pytest
from pytest_insta import SnapshotFixture
from beet import (
    run_beet,
)
EXAMPLES = [f for f in os.listdir("examples") if not f.startswith("nosnap_")]


@pytest.mark.parametrize("directory", EXAMPLES)
def test_build(snapshot: SnapshotFixture, directory: str):
    with run_beet(directory=f"examples/{directory}") as ctx:
        data_pack = snapshot("data_pack")
        resource_pack = snapshot("resource_pack")

        assert data_pack == ctx.data
        assert resource_pack == ctx.assets
