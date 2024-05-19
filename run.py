from pathlib import Path

from visualizer import ModuleVisualizer
from load import RepoLoader


repo_url = "https://github.com/pallets/flask.git"
script_path = Path(__file__).parent.resolve()
subject_path = script_path / "subject_repo"
files_path = subject_path / "src"
test_path = subject_path / "tests"

repo = RepoLoader(repo_url, subject_path, files_path, test_path)
repo.load_repo()

vis = ModuleVisualizer(repo)
artifacts = script_path / "artifacts"
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
    # rankdir="LR",
)
