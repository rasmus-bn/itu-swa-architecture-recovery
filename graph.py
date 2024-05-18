import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class Graph:
    def __init__(self, output_file, directed=True):
        if directed:
            self._graph = nx.DiGraph()
        else:
            self._graph = nx.Graph()
        self._output_file = output_file

    def create_figure(self):
        # Create a figure with 3 subplots in rows
        figure_scale = 1.5
        figure_heights = [
            15 * figure_scale,  # Graph
            0.1 * figure_scale,  # Scale title
            0.2 * figure_scale,  # Scale range
        ]
        self.fig, (self.ax_graph, self.ax_scale_title, self.ax_color_range) = (
            plt.subplots(
                nrows=3,
                ncols=1,
                figsize=(20 * figure_scale, sum(figure_heights) * figure_scale),
                gridspec_kw={
                    "height_ratios": figure_heights,
                    "width_ratios": [1 * figure_scale],
                    "wspace": 0,
                    "hspace": 0.1,
                },
            )
        )

    def add_node(self, node, size=1, color=None, weight=1):
        return self._graph.add_node(node, size=size, color=color, weight=weight)

    def add_edge(self, node1, node2, weight=1, color=None):
        return self._graph.add_edge(node1, node2, weight=weight, color=color)

    def _plot_color_legend(self, legend_desc, cmap_name):
        # This function was taken and modified from the matplotlib documentation:
        # https://matplotlib.org/stable/users/explain/colors/colormaps.html#grayscale-conversion
        gradient = np.linspace(0, 1, 256)
        gradient = np.vstack((gradient, gradient))

        # Create figure and adjust figure height to number of colormaps
        # fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh, left=0.2, right=0.99)
        self.ax_scale_title.set_title(legend_desc, fontsize=20)

        self.ax_color_range.imshow(
            gradient, aspect="auto", cmap=mpl.colormaps[cmap_name]
        )

        # Turn off *all* ticks & spines, not just the ones with colormaps.
        self.ax_scale_title.set_axis_off()
        self.ax_color_range.set_axis_off()

    def plot(self):
        self.create_figure()
        # Extract node weights
        weights = np.array(
            [self._graph.nodes[node]["weight"] for node in self._graph.nodes]
        )
        min_node_weight = min(weights)
        max_node_weight = max(weights)
        # Normalize weights to [0, 1]
        norm = plt.Normalize(vmin=min_node_weight, vmax=max_node_weight)
        # Create a colormap. See https://matplotlib.org/stable/users/explain/colors/colormaps.html#sequential
        cmap = plt.get_cmap("plasma")
        # Map weights to colors using the colormap
        node_colors = cmap(norm(weights))
        node_colors = [self._graph.nodes[node]["color"] for node in self._graph.nodes]

        # Get node sizes
        node_sizes = [self._graph.nodes[node]["size"] for node in self._graph.nodes]

        # Get edge weights and colors
        edge_weights = [self._graph.edges[edge]["weight"] for edge in self._graph.edges]
        edge_colors = [self._graph.edges[edge]["color"] for edge in self._graph.edges]

        # Draw the graph
        pos = nx.spring_layout(self._graph)
        nx.draw(
            self._graph,
            pos,
            with_labels=True,
            node_size=node_sizes,
            node_color=node_colors,
            edge_color=edge_colors,
            width=edge_weights,
            ax=self.ax_graph,
        )

        self._plot_color_legend(
            f"Color scale from {min_node_weight} (left) to {max_node_weight} (right)",
            "plasma",
        )

        # Show the plot
        plt.savefig(self._output_file)


if __name__ == "__main__":
    # Create a directed graph
    G = Graph("graph.png", directed=True)

    # Add nodes with attributes
    G.add_node(1, size=1000, color="red", weight=1)
    G.add_node(2, size=500, color="blue", weight=2)
    G.add_node(3, size=800, color="green", weight=3)
    G.add_node(4, size=1000, color="red", weight=4)
    G.add_node(5, size=500, color="blue", weight=5)
    G.add_node(6, size=800, color="green", weight=6)
    G.add_node(7, size=1000, color="red", weight=7)
    G.add_node(8, size=500, color="blue", weight=8)
    G.add_node(9, size=800, color="green", weight=9)
    G.add_node(10, size=1000, color="red", weight=10)
    G.add_node(11, size=500, color="blue", weight=11)
    G.add_node(12, size=800, color="green", weight=12)

    # Add edges with attributes
    G.add_edge(1, 2, weight=10, color="black")
    G.add_edge(2, 3, weight=4, color="orange")
    G.add_edge(3, 1, weight=1, color="purple")

    G.plot()

    # # Extract node weights
    # weights = np.array([G.nodes[node]["weight"] for node in G.nodes])
    # # Normalize weights to [0, 1]
    # min_node_weight = min(weights)
    # max_node_weight = max(weights)
    # norm = plt.Normalize(vmin=min_node_weight, vmax=max_node_weight)
    # # Create a colormap. See https://matplotlib.org/stable/users/explain/colors/colormaps.html#sequential
    # cmap = plt.get_cmap("plasma")
    # # Map weights to colors using the colormap
    # node_colors = cmap(norm(weights))

    # # Get node sizes and colors
    # node_sizes = [G.nodes[node]["size"] for node in G.nodes]
    # # node_colors = [G.nodes[node]["color"] for node in G.nodes]

    # # Get edge weights and colors
    # edge_weights = [G.edges[edge]["weight"] for edge in G.edges]
    # edge_colors = [G.edges[edge]["color"] for edge in G.edges]

    # all_scale = 0.85

    # # Create a figure with two subplots
    # figure_heights = [
    #     15 * all_scale,  # Graph
    #     0.1 * all_scale,  # Scale title
    #     0.2 * all_scale,  # Scale range
    # ]
    # fig, (ax_graph, ax_scale_title, ax_color_range) = plt.subplots(
    #     nrows=3,
    #     ncols=1,
    #     figsize=(20 * all_scale, sum(figure_heights) * all_scale),
    #     gridspec_kw={
    #         "height_ratios": figure_heights,
    #         "width_ratios": [1 * all_scale],
    #         "wspace": 0,
    #         "hspace": 0.1,
    #     },
    # )

    # # Draw the graph
    # pos = nx.spring_layout(G)
    # nx.draw(
    #     G,
    #     pos,
    #     with_labels=True,
    #     node_size=node_sizes,
    #     node_color=node_colors,
    #     edge_color=edge_colors,
    #     width=edge_weights,
    #     ax=ax_graph,
    # )

    # def plot_color_legend(legend_desc, cmap_name):
    #     # This function was taken and modified from the matplotlib documentation:
    #     # https://matplotlib.org/stable/users/explain/colors/colormaps.html#grayscale-conversion
    #     gradient = np.linspace(0, 1, 256)
    #     gradient = np.vstack((gradient, gradient))

    #     # Create figure and adjust figure height to number of colormaps
    #     # fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh, left=0.2, right=0.99)
    #     ax_scale_title.set_title(legend_desc, fontsize=20)

    #     ax_color_range.imshow(gradient, aspect="auto", cmap=mpl.colormaps[cmap_name])

    #     # Turn off *all* ticks & spines, not just the ones with colormaps.
    #     ax_scale_title.set_axis_off()
    #     ax_color_range.set_axis_off()

    # plot_color_legend("Color scale from low (left) to high (right)", "plasma")

    # # Show the plot
    # plt.savefig("graph.png")

    # # Create a figure with two subplots
    # fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5))

    # # Draw the graph on the first subplot
    # pos = nx.spring_layout(G)
    # nx.draw(
    #     G,
    #     pos,
    #     with_labels=True,
    #     node_size=node_sizes,
    #     node_color=node_colors,
    #     edge_color=edge_colors,
    #     width=edge_weights,
    #     ax=ax1,
    # )

    # # Plot the color scale on the second subplot
    # gradient = np.linspace(0, 1, 256)
    # gradient = np.vstack((gradient, gradient))
    # ax2.imshow(gradient, aspect="auto", cmap=cmap)
    # ax2.set_axis_off()

    # # Adjust the spacing between subplots
    # plt.subplots_adjust(wspace=0.1)

    # # Save the plot
    # plt.savefig("graph_with_color_scale.png")
