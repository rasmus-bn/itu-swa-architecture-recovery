import pygraphviz as pgv
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex
from load import Module, ModuleTypes, RepoLoader


class Normalizer:
    def __init__(self, data: list, new_min, new_max) -> None:
        self.data = data
        self.min = min(data)
        self.max = max(data)
        self._min_max_diff = self.max - self.min
        self.new_min = new_min
        self.new_max = new_max
        self._new_min_max_diff = self.new_max - self.new_min

    def normalize(self, value):
        return self.new_min + (value - self.min) * (self._new_min_max_diff) / (
            self._min_max_diff
        )


class ModuleVisualizer:
    def __init__(
        self,
        repo: RepoLoader,
    ) -> None:
        self.repo = repo
        self.min_node_size = 0.2
        self.max_node_size = 1
        self.mean_node_size = (self.max_node_size + self.min_node_size) / 2
        self.int_modules = [
            module
            for module in repo.modules_store.values()
            if module.mod_type == ModuleTypes.INTERNAL
        ]
        self.color_norm_int = Normalizer(
            [module.import_count for module in self.int_modules],
            0,
            1,
        )
        self.loc_size_norm = Normalizer(
            [file.loc for file in self.repo.files],
            self.min_node_size,  # Not allowing nodes of size 0
            self.max_node_size,
        )

        self.ext_modules = [
            module
            for module in repo.modules_store.values()
            if module.mod_type == ModuleTypes.EXTERNAL
        ]
        self.color_norm_ext = Normalizer(
            [module.import_count for module in self.ext_modules],
            0,
            1,
        )

    def _get_node_color(self, value, cmap_name: str):
        cmap = plt.get_cmap(cmap_name)
        color = list(cmap(value))

        adjuster = 3  # lower = more white
        for i in range(3):
            color[i] = color[i] + ((1 - color[i]) / adjuster)

        return rgb2hex(tuple(color))

    def _add_node(
        self,
        graph: pgv.AGraph,
        module: Module,
        color=None,
        cmap_name=None,
        size=None,
        size_adjuster=1,
        fontsize=14,
        xlabel=False,
    ):
        if not color:
            color_norm = (
                self.color_norm_int
                if module.mod_type == ModuleTypes.INTERNAL
                else self.color_norm_ext
            )
            color = self._get_node_color(
                color_norm.normalize(module.import_count), cmap_name
            )

        if not size:
            if module.mod_type == ModuleTypes.INTERNAL:
                size = self.loc_size_norm.normalize(module.python_file.loc)
            else:
                size = self.mean_node_size

        graph.add_node(
            module.id,
            fixedsize="true",
            height=size * size_adjuster,
            width=size * size_adjuster,
            color=color,
            fillcolor=color,
            style="filled",
            shape=(
                "circle" if module.mod_type == ModuleTypes.INTERNAL else "box"
            ),
            fontsize=fontsize,
            label="" if xlabel else module.id,
            xlabel=module.id if xlabel else "",
        )

    def visualize(
        self,
        output_file: str,
        graph_layout="dot",
        include_internal_dependencies: bool = True,
        int_color=None,
        int_cmap="plasma",
        int_size=None,
        int_xlabels=False,
        include_external_dependencies: bool = True,
        ext_color=None,
        ext_cmap="plasma",
        ext_size=None,
        ext_xlabels=False,
        node_size_adjuster=1,
        fontsize=14,
        padding=0.8,
        **kwargs,
    ):
        graph = pgv.AGraph(
            directed=True,
            strict=True,
            pad=padding,
            **kwargs,
        )

        # legend_pos = "0"
        # graph.add_node(
        #     "[least referenced]",
        #     fixedsize="true",
        #     height=0.5 * node_size_adjuster,
        #     width=0.5 * node_size_adjuster,
        #     color=self._get_node_color(1, int_cmap),
        #     fillcolor=self._get_node_color(1, int_cmap),
        #     style="filled",
        #     shape="circle",
        #     fontsize=fontsize,
        #     pos=legend_pos,
        # )
        # graph.add_node(
        #     "[mean referenced]",
        #     fixedsize="true",
        #     height=0.5 * node_size_adjuster,
        #     width=0.5 * node_size_adjuster,
        #     color=self._get_node_color(0.5, int_cmap),
        #     fillcolor=self._get_node_color(0.5, int_cmap),
        #     style="filled",
        #     shape="circle",
        #     fontsize=fontsize,
        #     pos=legend_pos,
        # )
        # graph.add_node(
        #     "[most referenced]",
        #     fixedsize="true",
        #     height=0.5 * node_size_adjuster,
        #     width=0.5 * node_size_adjuster,
        #     color=self._get_node_color(0.9, int_cmap),
        #     fillcolor=self._get_node_color(0.9, int_cmap),
        #     style="filled",
        #     shape="circle",
        #     fontsize=fontsize,
        #     pos=legend_pos,
        # )

        for module in self.int_modules:
            self._add_node(
                graph,
                module,
                color=int_color,
                cmap_name=int_cmap,
                size=int_size,
                size_adjuster=node_size_adjuster,
                fontsize=fontsize,
                xlabel=int_xlabels,
            )
        if include_external_dependencies:
            for module in self.ext_modules:
                self._add_node(
                    graph,
                    module,
                    color=ext_color,
                    cmap_name=ext_cmap,
                    size=ext_size,
                    size_adjuster=node_size_adjuster,
                    fontsize=fontsize,
                    xlabel=ext_xlabels,
                )

        for file in self.repo.files:
            for module in file.imports:
                module: Module
                if (
                    module.mod_type == ModuleTypes.INTERNAL
                    and include_internal_dependencies
                ):
                    graph.add_edge(
                        file.module_id,
                        module.id,
                        weight=1,
                        color="blue",
                        arrowsize=0.5,
                    )
                if (
                    module.mod_type == ModuleTypes.EXTERNAL
                    and include_external_dependencies
                ):
                    graph.add_edge(
                        file.module_id,
                        module.id,
                        weight=1,
                        color="red",
                        arrowsize=0.5,
                    )

        graph.layout(prog=graph_layout)
        graph.draw(output_file)
