import sys
import PyQt5.QtWidgets as qt
from Load_and_create_graph import Graph
from Paint_Graph import Paint
from Latin_composition import Hamilton_cycle
from Branch_and_bound import Hamilton_path

G = Graph()
P = Paint()
HC = Hamilton_cycle()
HP = Hamilton_path()


class Program_GUI():
    app = qt.QApplication(sys.argv)
    root = qt.QWidget()
    root2 = qt.QWidget()

    table = qt.QTableWidget(root2)
    table.setGeometry(0, 0, 1500, 1000)
    table.show()
    G.table = table

    mbx = qt.QMessageBox(root)
    mbx.setWindowTitle("Внимание!")
    mbx.setFixedWidth(500)
    mbx.setFixedHeight(500)
    P.mbx = mbx
    HC.mbx = mbx
    HP.mbx = mbx

    table_matrix_of_graph = qt.QTableWidget(root)
    table_matrix_of_graph.setGeometry(5, 60, 630, 500)
    table_matrix_of_graph.show()

    G.table_matrix_of_graph = table_matrix_of_graph# связка с list из класса Graph

    list_item = qt.QListWidgetItem()
    HP.list_item = list_item

    list_cycle_of_gamilt = qt.QListWidget(root)
    list_cycle_of_gamilt.setGeometry(660, 60, 400, 500)
    list_cycle_of_gamilt.show()
    HC.list_cycle_of_gamilt = list_cycle_of_gamilt
    HP.list_cycle_of_gamilt = list_cycle_of_gamilt

    list_of_different_graphs = qt.QListWidget(root)
    list_of_different_graphs.setGeometry(1100, 60, 250, 100)
    list_of_different_graphs.show()
    HC.list_of_different_graphs = list_of_different_graphs
    HP.list_of_different_graphs = list_of_different_graphs
    P.list_of_different_graphs = list_of_different_graphs

    lb_notice_for_count_of_nodes = qt.QLabel('Коллчество вершин:', root)
    lb_notice_for_count_of_nodes.move(1090, 12)
    lb_notice_for_count_of_nodes.show()

    btn_search_cycle = None
    btn_load = None
    btn_clear_matrix = None
    btn_clear_cycle = None
    btn_paint_graph = None

    count_of_nodes = qt.QLineEdit(root)
    count_of_nodes.move(1200, 10)
    count_of_nodes.show()
    P.count_of_nodes = count_of_nodes
    # HP.count_of_nodes = count_of_nodes
    HC.count_of_nodes = count_of_nodes

    button_group = qt.QButtonGroup(root)

    normal_draw = qt.QRadioButton("Обычная прорисовка", root)
    normal_draw.setGeometry(1100, 190 , 150, 20)
    normal_draw.setChecked(True)
    normal_draw.setEnabled(True)
    normal_draw.show()
    P.normal_draw = normal_draw

    circular_draw = qt.QRadioButton("Круговая прорисовка", root)
    circular_draw.setGeometry(1100, 220 , 150, 20)
    circular_draw.show()
    P.circular_draw = circular_draw

    random_draw = qt.QRadioButton("Рандомная прорисовка", root)
    random_draw.setGeometry(1100 ,250, 150, 20)
    random_draw.show()

    def __init__(self):
        self.root.setWindowTitle('G - algorithm')
        self.root.showMaximized()
        self.root2.showMaximized()
        self.config_btns()
        self.config_list()
        # self.config_radio_btns()

    def config_btns(self):
        self.btn_load = qt.QPushButton( 'Загрузить граф', self.root)
        self.btn_load.clicked.connect(G.load_from_file)
        self.btn_load.setFixedSize(100, 50)
        self.btn_load.move(250, 5)
        self.btn_load.show()

        self.btn_search_cycle = qt.QPushButton('Метод ветвей и границ', self.root)
        self.btn_search_cycle.clicked.connect(HP.find_cycle)
        self.btn_search_cycle.setFixedSize(150, 50)
        self.btn_search_cycle.move(660, 5)
        self.btn_search_cycle.show()

        self.btn_search_cycle = qt.QPushButton('Латинская композиция', self.root)
        self.btn_search_cycle.clicked.connect(HC.find_cycle)
        self.btn_search_cycle.setFixedSize(150, 50)
        self.btn_search_cycle.move(910, 5)
        self.btn_search_cycle.show()

        self.btn_clear_matrix = qt.QPushButton('Очистить', self.root)
        self.btn_clear_matrix.setEnabled(False)
        self.btn_clear_matrix.clicked.connect(self.clear_matrix)
        self.btn_clear_matrix.setFixedSize(100, 50)
        self.btn_clear_matrix.move(250, 580)
        self.btn_clear_matrix.show()

        self.btn_clear_cycle = qt.QPushButton('Очистить', self.root)
        self.btn_clear_cycle.clicked.connect(self.clear_cycle)
        self.btn_clear_cycle.setEnabled(False)
        self.btn_clear_cycle.setFixedSize(100, 50)
        self.btn_clear_cycle.move(830, 580)
        self.btn_clear_cycle.show()

        self.btn_paint_graph = qt.QPushButton('Нарисовать граф', self.root)
        self.btn_paint_graph.clicked.connect(P.paint_graph)
        self.btn_paint_graph.setFixedSize(100, 50)
        self.btn_paint_graph.move(1100, 300)
        self.btn_paint_graph.show()

        #Связка с кнопками из Graph, это необходимо для избежания циклического импорта
        G.btn_clear_matrix = self.btn_clear_matrix
        G.btn_paint_graph = self.btn_paint_graph
        G.btn_search_cycle = self.btn_search_cycle
        HP.btn_clear_cycle = self.btn_clear_cycle
        HC.btn_clear_cycle = self.btn_clear_cycle

    def config_list(self):
        self.list_of_different_graphs.addItem('Сhordal cycle graph(Хордальный граф)')
        self.list_of_different_graphs.addItem( 'Ladder graph (Лестничный граф)')
        self.list_of_different_graphs.addItem( 'Сomplete graph(Полный граф)')
        self.list_of_different_graphs.addItem( 'Cycle graph(Циклический граф)')

    def clear_matrix(self):
        G.graph_list.clear()
        G.nodes.clear()
        G.edges.clear()
        G.latin_dict.clear()
        self.table_matrix_of_graph.clear()
        self.btn_clear_matrix.setEnabled(False)

    def clear_cycle(self):
        HC.graph = None
        HC.latin_matrix = {}
        HC.count_nodes = None
        HC.all_matrix = {}
        HC.template_matrix = {}
        self.list_cycle_of_gamilt.clear()
        self.btn_clear_cycle.setEnabled(False)