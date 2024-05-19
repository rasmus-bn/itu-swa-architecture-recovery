from pathlib import Path

from visualizer import ModuleVisualizer
from loader import RepoLoader


repo_url = "https://github.com/pallets/flask.git"
local_repo_root = Path(__file__).parent.parent.resolve()
cloned_path = local_repo_root / "subject_repo"
files_path = cloned_path / "src"
test_path = cloned_path / "tests"

repo = RepoLoader(repo_url, cloned_path, files_path, test_path)
repo.load_repo()

vis = ModuleVisualizer(repo)
artifacts = local_repo_root / "artifacts"
artifacts.mkdir(exist_ok=True, parents=True)
vis.visualize(
    output_file=artifacts / "internal-dependencies.png",
    graph_layout="circo",
    include_internal_dependencies=True,
    include_external_dependencies=False,
    node_size_adjuster=1.7,
    fontsize=25,
    padding=1.8,
    # rankdir="BT",
)
vis.visualize(
    output_file=artifacts / "external-dependencies.png",
    graph_layout="fdp",
    include_internal_dependencies=False,
    int_color="dodgerblue",
    int_size=vis.mean_node_size,
    # int_xlabels=True,
    include_external_dependencies=True,
    fontsize=20,
    rankdir="LR",
)
vis.visualize(
    output_file=artifacts / "spaghetti-dependencies.png",
    graph_layout="fdp",
    include_internal_dependencies=True,
    int_color="dodgerblue",
    # int_cmap="plasma",
    int_size=vis.mean_node_size,
    # int_xlabels=True,
    include_external_dependencies=True,
    # ext_cmap="gnuplot",
    ext_color="firebrick1",
    fontsize=25,
    arrow_head_size=0.5,
    # rankdir="LR",
)
