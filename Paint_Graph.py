import networkx as nx
import matplotlib.pyplot as plt
from Load_and_create_graph import Graph

G = Graph()

class Paint():
    list_of_different_graphs = None
    count_of_nodes = None
    mbx = None
    normal_draw = None
    circular_draw = None

    def paint_graph(self):

        if G.graph_list:
            nodes = list(range(len(G.graph_list)))
            graph = nx.Graph()
            graph.add_nodes_from(nodes)
            graph.add_edges_from(G.edges)

        elif self.count_of_nodes.text().isdigit():
            if int(self.count_of_nodes.text()) > 0:
                graph_from_list = self.list_of_different_graphs.currentRow()
                if graph_from_list == 0:
                    graph = nx.chordal_cycle_graph(int(self.count_of_nodes.text()))
                elif graph_from_list == 1:
                    graph = nx.ladder_graph(int(self.count_of_nodes.text()))
                elif graph_from_list == 2:
                    graph = nx.complete_graph(int(self.count_of_nodes.text()))
                elif graph_from_list == 3:
                    graph = nx.cycle_graph(int(self.count_of_nodes.text()))
                else:
                    self.mbx.setText("Выберите граф!")
                    self.mbx.show()
                    return 0
            else:
                self.mbx.setText("Количество вершин должно быть больше нуля!")
                self.mbx.show()
                return 0
        else:
            self.mbx.setText("Количество врешин должно быть числом!")
            self.mbx.show()
            return 0

        if self.normal_draw.isChecked():
            nx.draw(graph)
        elif self.circular_draw.isChecked():
            nx.draw_circular(graph)
        else:
            nx.draw_random(graph)

        plt.show()