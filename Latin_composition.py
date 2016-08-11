from Load_and_create_graph import Graph
from copy import deepcopy
import networkx as nx
from time import time

g = Graph()


class Hamilton_cycle():
    list_cycle_of_gamilt = None
    list_of_different_graphs = None
    btn_clear_cycle = None

    count_of_nodes = None
    mbx = None

    graph = None
    latin_matrix = {}
    count_nodes = None
    all_matrix = {}
    template_matrix = {}
    sum_paths = []

    def init(self):
        self.latin_matrix = g.latin_dict.copy()

        self.count_nodes = len(g.graph_list)
        if self.count_nodes == 0:
            self.count_nodes = int(self.count_of_nodes.text())

        if self.latin_matrix:
            for k,v in self.latin_matrix.items():
                for i in range(len(v)):
                    if v[i] != "*":
                        v[i] = [[k, i]]

                while "*" in v:
                    v.remove("*")
        else:
            graph_from_list = self.list_of_different_graphs.currentRow()
            if graph_from_list == 0:
                self.graph = nx.chordal_cycle_graph(self.count_nodes)
            elif graph_from_list == 1:
                self.graph = nx.ladder_graph(self.count_nodes)
                self.count_nodes += self.count_nodes
            elif graph_from_list == 2:
                self.graph = nx.complete_graph(self.count_nodes)
            elif graph_from_list == 3:
                self.graph = nx.cycle_graph(self.count_nodes)
            else:
                self.mbx.setText("Выберите граф!")
                self.mbx.show()
                return 0

            for i in range(self.count_nodes):
                self.latin_matrix[i] = []


            for i in self.graph.edges():
                if ([[i[0], i[1]]] not in self.latin_matrix[i[0]]):
                    if i[0] != i[+1]:
                        self.latin_matrix[i[0]].append([[i[0], i[1]]])
                        self.latin_matrix[i[1]].append([[i[1], i[0]]])


        #Создаем пустую матрицу для последующего заполнения
        for i in range(self.count_nodes):
            l = []
            for j in range(self.count_nodes):
                l.append([])
            self.template_matrix[i] = l.copy()
        #=========================================

        self.all_matrix[1] = self.latin_matrix

    def find_cycle(self):
        inspection = self.init()
        if inspection == 0:
            return 0
        self.method_latin_composition()


    def method_latin_composition(self):
        self.btn_clear_cycle.setEnabled(True)
        # mbx.showinfo(message=self.latin_matrix)

        def matrix_multiply(m1, m2, m1_index, m2_index):
            ''' Умножение матрицы m1 на m2 штрих! матрицы - словари'''

            result_matrix = deepcopy(self.template_matrix)

            inside = False
            if (m1_index + m2_index) == self.count_nodes:
                last_iteration = True
            else:
                last_iteration = False

            m2_copy = deepcopy(m2)#Создаем копию дабы не портить оригинал

            #Делаем из матрицы m2 матрицу m2 штрих
            for k,v in m2_copy.items():
                for i in v:
                    for j in i:
                        del j[0]
            #=====================================
            m1_row = 0
            for k, v in m1.items():
                m1_row += 1
                #Цикл по матрице1
                for i in range(len(v)):    #Квадрат

                    for j in v[i]:  #Список
                        m2_row = m2_copy.get(j[-1])#Строка матрицы2 штрих
                        #Цикл по матрице2 штрих
                        for g in m2_row: #Квадрат

                            for e in g: #Список
                                if last_iteration:
                                    r = range(len(e)-1)
                                else:
                                    r = range(len(e))
                                for h in r: #Буква
                                    if e[h] not in j:
                                        inside = False
                                    else:
                                        inside = True
                                        break

                                if inside is False:
                                    l = []
                                    l.extend(j)
                                    l.extend(e)
                                    new_row = result_matrix.get(k)#Создается ссылочная зависимасть
                                    #При изменении new_row меняется ключь в словаре result_matrix
                                    new_row[l[-1]].append(l.copy())
                    print("Матрица{0}: {1} ячейка вычислена!".format(m1_index+m2_index, i))

                if last_iteration:
                    g = Graph()
                    if g.graph_list:
                        sum_path = 0
                        for l in result_matrix[0][0]:
                            for i in range(len(l)-1):
                                sum_path += g.graph_list[l[i]][l[i+1]]
                            self.sum_paths.append(sum_path)
                            sum_path = 0
                    return result_matrix

                print("Матрица{0}: {1} строка вычислена!".format(m1_index+m2_index, m1_row))
                print("========================================================================")

            return result_matrix
        #Эмуляция цикла while-do
        start = time()
        while True:
            all_keys = list(self.all_matrix.keys())#Достает "индекс"(||M||n -индекс матрицы) последней вычисленной матрицы
            all_keys.sort()
            last_key = all_keys[-1]
            global matrix_index
            matrix_index = last_key + last_key

            #Если индекс матрицы которая будет вычислена не превышает колич-во верши
            if matrix_index <= self.count_nodes:
                m2 = deepcopy(self.all_matrix[last_key])#Достается последняя вычисленная матрица
                #Умножается последняя вычисленная матрица и ее копия
                result_matrix = matrix_multiply(self.all_matrix[last_key], m2, last_key, last_key)
                self.all_matrix[matrix_index] = result_matrix

                if matrix_index == self.count_nodes:
                    result_row = result_matrix[0]
                    end = time()
                    algorithm_time = round(end - start, 5)
                    try:
                        self.list_cycle_of_gamilt.addItem("Метод латинской композиции: ")
                        self.list_cycle_of_gamilt.addItem("--------------------------")
                        if g.graph_list:
                            min_sum = min(self.sum_paths)
                            min_sum_index = self.sum_paths.index(min_sum)
                            self.list_cycle_of_gamilt.addItem("Стоимость пути: "+ str(min_sum))
                            self.list_cycle_of_gamilt.addItem(str(result_row[0][min_sum_index]))
                            self.clear_all()
                        else:
                            self.list_cycle_of_gamilt.addItem(str(result_row[0][0]))
                            self.clear_all()

                        self.list_cycle_of_gamilt.addItem("Время: " + str(algorithm_time))
                        self.list_cycle_of_gamilt.addItem("=============================================")
                    except:
                        self.list_cycle_of_gamilt.addItem("Нет цикла!")
                        self.clear_all()
                    return 0

            else:
                need_multiply = {}
                need_index = self.count_nodes - last_key
                if need_index in self.all_matrix.keys():
                    result_matrix = matrix_multiply(self.all_matrix[last_key], self.all_matrix[need_index],
                                                    last_key, need_index)
                    result_row = result_matrix[0]
                    end = time()
                    algorithm_time = round(end - start, 5)
                    try:
                        self.list_cycle_of_gamilt.addItem("Метод латинской композиции: ")
                        self.list_cycle_of_gamilt.addItem("--------------------------")
                        if g.graph_list:
                            min_sum = min(self.sum_paths)
                            min_sum_index = self.sum_paths.index(min_sum)
                            self.list_cycle_of_gamilt.addItem("Стоимость пути: "+ str(min_sum))
                            self.list_cycle_of_gamilt.addItem(str(result_row[0][min_sum_index]))
                            self.clear_all()
                        else:
                            self.list_cycle_of_gamilt.addItem( str(result_row[0][0]))
                            self.clear_all()

                        self.list_cycle_of_gamilt.addItem("Время: " + str(algorithm_time))
                        self.list_cycle_of_gamilt.addItem( "============================================")
                    except:
                        self.list_cycle_of_gamilt.addItem( "Нет цикла!")
                        self.clear_all()
                    return 0

                while need_index != 0:
                    for key in reversed(all_keys):
                        if key <= need_index:
                            need_multiply[key] = self.all_matrix[key]
                            need_index -= key
                            break

                key1 = list(need_multiply.keys())[0]#Достает самый первый ключ
                result_matrix = need_multiply[key1]
                for i in range(len(list(need_multiply.keys()))):
                    if i == 0:
                        continue
                    key2 = list(need_multiply.keys())[i]
                    result_matrix = matrix_multiply(need_multiply[key2], result_matrix, key2, key1)
                    key1 = key1 + key2

                result_matrix = matrix_multiply(self.all_matrix[last_key], result_matrix,
                                                last_key, key1)
                result_row = result_matrix[0]
                end = time()
                algorithm_time = round(end - start, 5)
                try:
                    self.list_cycle_of_gamilt.addItem("Метод латинской композиции: ")
                    self.list_cycle_of_gamilt.addItem("--------------------------")
                    if g.graph_list:
                        min_sum = min(self.sum_paths)
                        min_sum_index = self.sum_paths.index(min_sum)
                        self.list_cycle_of_gamilt.addItem( "Стоимость пути: "+ str(min_sum))
                        self.list_cycle_of_gamilt.addItem( str(result_row[0][min_sum_index]))
                        self.clear_all()
                    else:
                        self.list_cycle_of_gamilt.addItem( str(result_row[0][0]))
                        self.clear_all()

                    self.list_cycle_of_gamilt.addItem( "Время: " + str(algorithm_time))
                    self.list_cycle_of_gamilt.addItem( "==================================================")
                except:
                    self.list_cycle_of_gamilt.addItem( "Нет цикла!")
                    self.clear_all()
                return 0

            #Если индекс матрицы == количеству вершин графа, то
            if self.count_nodes == matrix_index:
                break

    def clear_all(self):
        self.count_of_nodes = None
        self.graph = None
        self.latin_matrix = {}
        self.count_nodes = None
        self.all_matrix = {}
        self.template_matrix = {}
        self.sum_paths = []