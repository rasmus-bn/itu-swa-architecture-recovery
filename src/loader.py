from pathlib import Path
import ast
import os
import re

from git import Repo


class PythonFile:
    def __init__(self, name: str, relative_path: Path, full_path: Path) -> any:
        self.name = name
        self.relative_path = relative_path
        self.full_path = full_path
        self.module_id = ".".join(list(relative_path.parts)).replace(".py", "")
        if self.name == "__init__.py":
            self.module_id = ".".join(list(relative_path.parts[:-1]))
        self.content = full_path.read_text()
        self.imports: list[any] = None
        self._ast: ast.AST = None
        self._loc = None

    @property
    def ast(self) -> ast.AST:
        if not self._ast:
            self._ast = ast.parse(self.content)
        return self._ast

    @property
    def loc(self) -> int:
        if not self._loc:
            self._loc = len(
                [
                    line
                    for line in self.content.splitlines()
                    if self.is_loc(line)
                ]
            )
        return self._loc

    @staticmethod
    def is_loc(line: str) -> bool:
        if not line:
            return False
        line = line.strip()
        if line.startswith("#"):
            return False
        if line == "'''" or line == '"""':
            return False
        if re.match(r"^[\)\]\}]*$", line):
            return False
        return True

    def load_imports(self, module_store: dict) -> list[any]:
        if self.imports:
            return self.imports
        self.imports = []

        def create_if_not_exist(module_name, mod_type):
            if mod_type == ModuleTypes.EXTERNAL:
                module_name = module_name.split(".")[0]
            if module_name not in module_store:
                module_store[module_name] = Module(module_name, mod_type)
            return module_store[module_name]

        for node in ast.walk(self.ast):
            module = None

            if isinstance(node, ast.Import):
                for module_import in node.names:
                    module = create_if_not_exist(
                        module_import.name, ModuleTypes.EXTERNAL
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0:
                    module = create_if_not_exist(
                        node.module, ModuleTypes.EXTERNAL
                    )
                else:
                    relative_path = ".".join(
                        list(self.relative_path.parts[: -node.level])
                    )
                    if node.module:
                        module_name = f"{relative_path}.{node.module}"
                    else:
                        module_name = relative_path
                    module = create_if_not_exist(
                        module_name, ModuleTypes.INTERNAL
                    )

            if module:
                self.imports.append(module)
                module.register_import()

        return self.imports


class ModuleTypes:
    # STANDARD = "standard library"
    EXTERNAL = "external library"
    INTERNAL = "internal module"


class Module:
    def __init__(
        self, id: str, mod_type: str, python_file: PythonFile = None
    ) -> any:
        self.id = id
        self.mod_type = mod_type
        self.python_file = python_file
        self.import_count = 0

    def register_import(self):
        self.import_count += 1


class RepoLoader:
    def __init__(
        self,
        repo_url: str,
        clone_path: str,
        src_path: str = None,
        test_path: str = None,
    ):
        self.repo_url = repo_url
        self.clone_path = Path(clone_path)
        self.src_path = Path(src_path if src_path else clone_path)
        self.test_path = Path(test_path) if test_path else None

        self.files: list[PythonFile] = []
        self.test_files: list[PythonFile] = []
        self.modules_store: dict[str, Module] = {}

    def _load_python_files(self, path):
        files = []
        for file in path.rglob("*.py"):
            relative_path = file.relative_to(path)
            file_name = file.name
            files.append(PythonFile(file_name, relative_path, file))
        return files

    def load_repo(self):
        if not self.clone_path.exists():
            self.clone_path.mkdir(exist_ok=True, parents=True)
        is_empty = not os.listdir(self.clone_path)
        if is_empty:
            Repo.clone_from(self.repo_url, self.clone_path)

        self.files = self._load_python_files(self.src_path)
        for file in self.files:
            self.modules_store[file.module_id] = Module(
                file.module_id, ModuleTypes.INTERNAL, file
            )

        for file in self.files:
            file.load_imports(self.modules_store)

        if self.test_path:
            self.test_files = self._load_python_files(self.test_path)


if __name__ == "__main__":
    repo_url = "https://github.com/pallets/flask.git"
    script_path = Path(__file__).parent.resolve()
    subject_path = script_path / "subject_repo"
    files_path = subject_path / "src"
    test_path = subject_path / "tests"

    repo = RepoLoader(repo_url, subject_path, files_path, test_path)

    repo.load_repo()
    mean_loc = sum([file.loc for file in repo.files]) / len(repo.files)
    print(mean_loc)
    mean_loc = sum([file.loc for file in repo.test_files]) / len(repo.files)
    print(mean_loc)
    # print(ast.dump(repo.files[2].ast, indent=2))
    ast_body = repo.files[2].ast.body
    module_names = [file.module_id for file in repo.files]
    module_names.sort()
    module_names.reverse()

    include_internal_nodes = False
    include_external_nodes = True

    import pygraphviz as pgv
    import matplotlib.pyplot as plt
    from matplotlib.colors import rgb2hex

    graph = pgv.AGraph(directed=True, strict=True, rankdir="LR", pad=0.8)
    min_imports = min(
        [module.import_count for module in repo.modules_store.values()]
    )
    max_imports = max(
        [module.import_count for module in repo.modules_store.values()]
    )

    def normalize(value):
        return (value - min_imports) / (max_imports - min_imports)

    def get_color(value):
        adjuster = 3  # lower = more white
        norm = normalize(value)
        cmap = plt.get_cmap("plasma")
        color = cmap(norm)
        color = list(color)
        for i in range(3):
            color[i] = color[i] + ((1 - color[i]) / adjuster)
        return rgb2hex(tuple(color))

    node_scaler = 5

    def add_node(module: Module):
        color = get_color(module.import_count)
        node_size = normalize(module.import_count) * node_scaler
        node_size = node_scaler / 7
        graph.add_node(
            module.id,
            fixedsize="true",
            height=node_size,
            width=node_size,
            color=color,
            fillcolor=color,
            style="filled",
            shape="circle"
            if module.mod_type == ModuleTypes.INTERNAL
            else "box",
        )

    for module_id, module in repo.modules_store.items():
        if module.mod_type == ModuleTypes.INTERNAL:
            add_node(module)
        if module.mod_type == ModuleTypes.EXTERNAL and include_external_nodes:
            add_node(module)

    def add_edge(consumer, owner, weight, color):
        graph.add_edge(
            consumer,
            owner,
            weight=weight,
            color=color,
            arrowhead="normal",
            arrowsize=0.5,
        )

    for file in repo.files:
        for module in file.imports:
            module: Module
            if (
                module.mod_type == ModuleTypes.INTERNAL
                and include_internal_nodes
            ):
                add_edge(file.module_id, module.id, 5, "blue")
            if (
                module.mod_type == ModuleTypes.EXTERNAL
                and include_external_nodes
            ):
                add_edge(file.module_id, module.id, 5, "red")

    graph.layout(prog="fdp")
    graph.draw("output_file3.png")

    print("done")
