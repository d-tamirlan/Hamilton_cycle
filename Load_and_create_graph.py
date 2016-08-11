import PyQt5.QtWidgets as qt
from copy import deepcopy


class Graph():

    table_matrix_of_graph = None
    table = None

    btn_clear_matrix = None
    btn_search_cycle = None
    btn_paint_graph = None

    lb_quantity_of_nodes = None
    lb_quantity_of_edges = None

    graph_list = []

    nodes = []
    edges = []
    latin_dict = {}

    Visited = []
    n = 0

    def load_from_file(self):
        lines = []
        # file = askopenfile()
        file = qt.QFileDialog.getOpenFileName()[0]
        if not file:
            return 0
        f = open(file, 'r')
        count = 0
        for line in f:
            line = line.strip()
            list_of_word =  line.split()#разлогает строку на слова и преобразует их в int! Обажаю Python!

            for i in range(len(list_of_word)):
                if list_of_word[i] != "*":
                    list_of_word[i] = int(list_of_word[i])

            self.graph_list.append(list_of_word)
            self.latin_dict[count] = list_of_word.copy()
            count += 1
            lines.append(line)
        f.close()

        f = open(file, 'r')
        l = list(enumerate(f))
        for i, line in l:
            line = line.strip()
            list_of_word =  line.split()

            self.table_matrix_of_graph.setColumnCount(len(list_of_word))
            self.table_matrix_of_graph.setRowCount(len(list_of_word))

            self.table.setColumnCount(len(list_of_word))
            self.table.setRowCount(len(list_of_word))

            for j in range(len(list_of_word)):
                self.table_matrix_of_graph.setItem(i, j, qt.QTableWidgetItem(list_of_word[j]))
                self.table.setItem(i, j, qt.QTableWidgetItem(list_of_word[j]))
        f.close()

        headers = list(range(len(self.graph_list)))
        headers = list(map(str, headers))
        self.table_matrix_of_graph.setHorizontalHeaderLabels(headers)
        self.table_matrix_of_graph.setVerticalHeaderLabels(headers)
        self.table_matrix_of_graph.resizeColumnsToContents()

        self.table.setHorizontalHeaderLabels(headers)
        self.table.setVerticalHeaderLabels(headers)
        self.table.resizeColumnsToContents()

        self.btn_clear_matrix.setEnabled(True)
        self.btn_paint_graph.setEnabled(True)
        self.btn_search_cycle.setEnabled(True)

        self.create_graph()

    def create_graph(self):
        self.nodes = list(range(len(self.graph_list)))
        graph_list = deepcopy(self.graph_list)
        edge = ()
        for i in range(len(graph_list)):
            for j in range(len(graph_list[i])):
                if graph_list[i][j] != "*" and graph_list[i][j] != None:
                    edge = (i, j)
                    self.edges.append(edge)
                    graph_list[i][j] = None
                    graph_list[j][i] = None
        graph_list = None