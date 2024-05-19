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
)
vis.visualize(
    output_file=artifacts / "external-dependencies--unfiltered.png",
    graph_layout="fdp",
    include_internal_dependencies=False,
    int_color="dodgerblue",
    int_size=vis.mean_node_size,
    include_external_dependencies=True,
    fontsize=22,
)
vis.visualize(
    output_file=artifacts / "external-dependencies--more-than-10-imports.png",
    graph_layout="fdp",
    include_internal_dependencies=False,
    int_color="dodgerblue",
    int_size=vis.mean_node_size,
    include_external_dependencies=True,
    fontsize=15,
    min_imports_threshold=11,
)
vis.visualize(
    output_file=artifacts / "external-dependencies--3-to-10-imports.png",
    graph_layout="fdp",
    include_internal_dependencies=False,
    int_color="dodgerblue",
    int_size=vis.mean_node_size,
    include_external_dependencies=True,
    fontsize=15,
    min_imports_threshold=4,
    max_imports_threshold=10,
)
vis.visualize(
    output_file=artifacts / "external-dependencies--less-than-3-imports.png",
    graph_layout="fdp",
    include_internal_dependencies=False,
    int_color="dodgerblue",
    int_size=vis.mean_node_size,
    include_external_dependencies=True,
    fontsize=18,
    max_imports_threshold=3,
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
    fontsize=15,
    arrow_head_size=0.7,
    # min_imports_threshold=4,
    # max_imports_threshold=10,
    # rankdir="LR",
)
