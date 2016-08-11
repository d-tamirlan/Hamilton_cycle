import Load_and_create_graph as lg
import copy as cp
import time as t

g = lg.Graph()

class Hamilton_path():

    list_cycle_of_gamilt = None
    list_of_different_graphs = None
    btn_clear_cycle = None
    mbx = None

    go_matrix = []
    not_go_matrix = []

    go_rows_cols = []
    not_go_rows_cols = []

    price = 0
    row_col = 0

    rows = {}
    cols = {}

    is_global_go_branch = True
    go_branch = True
    first_matrix = {0: {"rows": [], "cols": []}}

    all_go_branches = []
    all_not_go_branches = []

    first_iteration = True
    second_iteration = False

    branch_jump = False

    inf = float("inf")
    first_node = 0

    def init(self):
        graph_from_list = self.list_of_different_graphs.currentRow()

        if graph_from_list != -1:
            self.mbx.setText("Метод ветвей и границ не предназначен\nдля не взвешенных графов")
            self.mbx.show()
            return 0

        if not g.graph_list:
            self.mbx.setText("Выберите граф!")
            self.mbx.show()
            return 0

        #Заменяем все "*" на бесконечность чтобы функция min() не вызывала исключение из-зи строки
        for i in range(len((g.graph_list))):
            for j in range(len(g.graph_list[i])):
                if g.graph_list[i][j] == '*':
                    g.graph_list[i][j] = self.inf
        #=================================================

        #Задаем размерность столбцам т.к. они заполнятся по элементно
        #Строкам это не нужно т.к. они заполняются списками
        for i in g.graph_list:
            l = [None]* len(g.graph_list)
            self.first_matrix[0]["cols"].append(l)
        #==========================================

        l = None #Удаляем ссылочную зависимость и за одно освобождаем память

        #Формируем строки и столбцы отдельно, чтобы можно было применять функцию min() к столбцам
        for i in range(len(g.graph_list)):
            self.first_matrix[0]["rows"].append(g.graph_list[i])
            for j in range(len(g.graph_list[i])):
                self.first_matrix[0]["cols"][i][j] = g.graph_list[j][i]
        #===================================================

    def matrix_reduction(self, matrix):
        """Вычисление min строк и их вычитание из строк,
        Вычисление min столбцов и их вычитание из столбцов,
        Суммирование min-ов строк и стобцов"""

        sum_min_rows = 0
        sum_min_cols = 0
        min_rows_cols = {}
        row_keys = list(matrix["rows"])
        row_keys.sort()
        col_keys = list(matrix["cols"])
        col_keys.sort()

        if self.first_iteration:
            for i,row in enumerate(matrix["rows"]):
                min_row = min(row)
                if min_row != 0 and min_row != self.inf:
                    row[:] = [x-min_row for x in row]
                    for j in range(len(row)):
                        matrix["cols"][j][i] -= min_row
                    sum_min_rows += min_row

            for i,col in enumerate(matrix["cols"]):
                min_col = min(col)
                if min_col != 0 and min_col != self.inf:
                    col[:] = [x-min_col for x in col]
                    for j in range(len(row_keys)):
                        matrix["rows"][j][i] -= min_col

                    sum_min_cols += min_col
        else:
            for i,k in enumerate(row_keys):
                min_row = min(matrix["rows"][k])
                if min_row != 0 and min_row != self.inf:
                    matrix["rows"][k][:] = [x-min_row for x in matrix["rows"][k]]
                    for j in matrix["cols"]:
                        matrix["cols"][j][i] -= min_row
                    sum_min_rows += min_row

            for i,k in enumerate(col_keys):
                min_col = min(matrix["cols"][k])
                if min_col != 0 and min_col != self.inf:
                    matrix["cols"][k][:] = [x-min_col for x in matrix["cols"][k]]
                    for j in matrix["rows"]:
                        matrix["rows"][j][i] -= min_col

                    sum_min_cols += min_col
        sum_min = sum_min_rows + sum_min_cols

        if self.first_iteration:
            self.first_matrix[sum_min_rows+sum_min_cols] = self.first_matrix.pop(0)
            self.first_node = list(self.first_matrix.keys())[0]
            self.second_iteration = True
            for i,row in enumerate(matrix["rows"]):
                self.rows[i] = row
            for i,col in enumerate(matrix["cols"]):
                self.cols[i] = col
            matrix["rows"] = self.rows
            matrix["cols"] = self.cols
            return matrix

        elif self.second_iteration:
            self.all_go_branches[0].append(sum_min+self.first_node)
            self.all_go_branches[0].append([])
            self.second_iteration = False

        elif self.branch_jump:
            return 0

        else:
            if self.is_global_go_branch:
                if self.go_branch:
                    self.all_go_branches[-1].append(sum_min+self.all_go_branches[-3][2])
                    self.all_go_branches[-1].append([self.all_go_branches[-3][0]])
                    self.all_go_branches[-1][3].extend(self.all_go_branches[-3][3])
                else:
                    if len(self.all_go_branches) < 4:
                         self.all_go_branches[-1].append(sum_min+self.all_go_branches[-3][2])
                         self.all_go_branches[-1].append([])
                         self.all_go_branches[-1][3].extend(self.all_go_branches[-3][3])
                    else:
                        self.all_go_branches[-1].append(sum_min+self.all_go_branches[-4][2])
                        self.all_go_branches[-1].append([])
                        self.all_go_branches[-1][3].extend(self.all_go_branches[-4][3])
            else:
                if self.go_branch:
                    self.all_not_go_branches[-1].append(sum_min+self.all_not_go_branches[-3][2])
                    self.all_not_go_branches[-1].append([self.all_not_go_branches[-3][0]])
                    self.all_not_go_branches[-1][3].extend(self.all_not_go_branches[-3][3])
                else:
                    if len(self.all_not_go_branches) < 4:
                        self.all_not_go_branches[-1].append(sum_min+self.all_not_go_branches[-3][2])
                        self.all_not_go_branches[-1].append([])
                        self.all_not_go_branches[-1][3].extend(self.all_not_go_branches[-3][3])
                    else:
                        self.all_not_go_branches[-1].append(sum_min+self.all_not_go_branches[-4][2])
                        self.all_not_go_branches[-1].append([])
                        self.all_not_go_branches[-1][3].extend(self.all_not_go_branches[-4][3])

    def delete_col_row(self, matrix):
        """ Вычисление min-ов в строке и столбце с нулем,
        Суммирование min-ов,
        Выборка max из сумм min-ов,
        Удаление строки и столбца с 'нужным'
        (у которого сумма min-ов строки и стобца max-а) нулем"""
        row_keys = list(matrix["rows"].keys())
        row_keys.sort()
        col_keys = list(matrix["cols"].keys())
        col_keys.sort()
        min_rows_cols = {}
        for i,k in enumerate(row_keys):
            for j,col in enumerate(col_keys):
                if matrix["rows"][k][j] == 0:
                    matrix["rows"][k][j] = self.inf
                    matrix["cols"][col][i] = self.inf
                    min_row = min(matrix["rows"][k])
                    min_col = min(matrix["cols"][col])
                    min_rows_cols[min_row+min_col] = [i,j]
                    matrix["rows"][k][j] = 0
                    matrix["cols"][col][i] = 0

        delete_row_col = min_rows_cols[max(min_rows_cols)]

        if self.first_iteration:
            self.all_not_go_branches.append([(row_keys[delete_row_col[0]], col_keys[delete_row_col[1]]),
                                            False, max(min_rows_cols)+self.first_node, []])

            matrix["rows"][row_keys[delete_row_col[0]]][delete_row_col[1]] = self.inf
            matrix["cols"][col_keys[delete_row_col[1]]][delete_row_col[0]] = self.inf
            self.not_go_matrix.append(cp.deepcopy(matrix))

#===================================
        if self.is_global_go_branch and self.first_iteration is False:
            if self.go_branch:
                self.all_go_branches.append([(row_keys[delete_row_col[0]], col_keys[delete_row_col[1]]),
                            False, max(min_rows_cols)+self.all_go_branches[-1][2],[self.all_go_branches[-1][0]]])
                self.all_go_branches[-1][3].extend(self.all_go_branches[-2][3])

            else:
                self.all_go_branches.append([(row_keys[delete_row_col[0]], col_keys[delete_row_col[1]]),
                        False, max(min_rows_cols)+self.all_go_branches[-2][2],[]])
                self.all_go_branches[-1][3].extend(self.all_go_branches[-3][3])

            self.all_go_branches.append([(row_keys[delete_row_col[0]], col_keys[delete_row_col[1]]), False])

        if self.is_global_go_branch is False and self.first_iteration is False:
            if self.go_branch:
                self.all_not_go_branches.append([(row_keys[delete_row_col[0]], col_keys[delete_row_col[1]]),
                    False, max(min_rows_cols)+self.all_not_go_branches[-1][2],[self.all_not_go_branches[-1][0]]])
                self.all_not_go_branches[-1][3].extend(self.all_not_go_branches[-2][3])
            else:
                if len(self.all_not_go_branches) < 2:
                    self.all_not_go_branches.append([(row_keys[delete_row_col[0]], col_keys[delete_row_col[1]]),
                        False, max(min_rows_cols)+self.all_not_go_branches[-1][2],[]])
                    self.all_not_go_branches[-1][3].extend(self.all_not_go_branches[-2][3])
                else:
                    self.all_not_go_branches.append([(row_keys[delete_row_col[0]], col_keys[delete_row_col[1]]),
                        False, max(min_rows_cols)+self.all_not_go_branches[-2][2],[]])
                    self.all_not_go_branches[-1][3].extend(self.all_not_go_branches[-2][3])

            self.all_not_go_branches.append([(row_keys[delete_row_col[0]], col_keys[delete_row_col[1]]), False])
  #===================================
        if self.is_global_go_branch:
            if self.first_iteration:
                self.all_go_branches.append([(row_keys[delete_row_col[0]], col_keys[delete_row_col[1]]), False])
        else:
            if self.first_iteration:
                self.all_not_go_branches.append([(row_keys[delete_row_col[0]], col_keys[delete_row_col[1]]), False])

        matrix["rows"][row_keys[delete_row_col[0]]][delete_row_col[1]] = self.inf
        matrix["cols"][col_keys[delete_row_col[1]]][delete_row_col[0]] = self.inf

        if self.is_global_go_branch:
            if self.first_iteration is False:
                self.go_matrix.append(cp.deepcopy(matrix))
            else:
                self.first_iteration = False

        else:
            if self.first_iteration is False:
                self.not_go_matrix.append((cp.deepcopy((matrix))))
            else:
                self.first_iteration = False

        if col_keys[delete_row_col[1]] in matrix["rows"] and row_keys[delete_row_col[0]] in matrix["cols"]:
                col_index = col_keys.index(row_keys[delete_row_col[0]])
                row_index = row_keys.index(col_keys[delete_row_col[1]])
                matrix["rows"][col_keys[delete_row_col[1]]][col_index] = self.inf
                matrix["cols"][row_keys[delete_row_col[0]]][row_index] = self.inf

        for col in col_keys:
            del matrix["cols"][col][delete_row_col[0]]

        for row in row_keys:
            del matrix["rows"][row][delete_row_col[1]]

        del matrix["rows"][row_keys[delete_row_col[0]]]
        del matrix["cols"][col_keys[delete_row_col[1]]]

        if self.is_global_go_branch:
            self.go_matrix.append(cp.deepcopy(matrix))
        else:
            self.not_go_matrix.append(cp.deepcopy(matrix))

    def branch_and_bound_algorithm(self):
        self.btn_clear_cycle.setEnabled(True)

        start = t.time()

        self.rows = dict.fromkeys(range(len(self.first_matrix[0]["rows"])))
        self.cols = dict.fromkeys(range(len(self.first_matrix[0]["cols"])))

        matrix = self.matrix_reduction(cp.deepcopy(self.first_matrix[0]))
        self.delete_col_row(matrix)
        self.matrix_reduction(matrix)
        a = 0

        if self.all_go_branches[-1][2] <= self.all_not_go_branches[-1][2]:
            self.is_global_go_branch = True
            self.go_branch = True
            self.all_go_branches[-1][1] = True
            min_price = self.all_go_branches[-1][2]
        else:
            matrix = cp.deepcopy(self.not_go_matrix[0])
            self.is_global_go_branch = False
            self.go_branch = False
            self.all_not_go_branches[-1][1] = True
            min_price = self.all_not_go_branches[-1][2]
        count = 0
        while True:
            if self.branch_jump:
                self.subcycle_limitation(matrix)

                self.matrix_reduction(matrix)
                self.delete_col_row(matrix)
                count += 1
                print("Привидение матрицы " + str(count))
                self.branch_jump = False
                self.matrix_reduction(matrix)
            else:
                self.subcycle_limitation(matrix)

                self.branch_jump = True
                self.matrix_reduction(matrix)
                self.branch_jump = False

                self.delete_col_row(matrix)
                self.matrix_reduction(matrix)
                count += 1
                print("Привидение матрицы " + str(count))

            if self.is_global_go_branch:
                if self.all_go_branches[-1][2] <= self.all_go_branches[-2][2]:
                    self.is_global_go_branch = True
                    self.go_branch = True
                    self.all_go_branches[-1][1] = True
                    min_price = self.all_go_branches[-1][2]
                else:
                    matrix = cp.deepcopy(self.go_matrix[-2])
                    self.is_global_go_branch = True
                    self.go_branch = False
                    self.all_go_branches[-2][1] = True
                    min_price = self.all_go_branches[-2][2]

            else:
                if self.all_not_go_branches[-1][2] <= self.all_not_go_branches[-2][2]:
                    self.is_global_go_branch = False
                    self.go_branch = True
                    self.all_not_go_branches[-1][1] = True
                    min_price = self.all_not_go_branches[-1][2]
                else:
                    matrix = cp.deepcopy(self.not_go_matrix[-2])
                    self.is_global_go_branch = False
                    self.go_branch = False
                    self.all_not_go_branches[-2][1] = True
                    min_price = self.all_not_go_branches[-2][2]

            go_false_prices = {}
            not_go_false_prices = {}
            for i in range(len(self.all_go_branches)):
                if self.all_go_branches[i][1] is False:
                    go_false_prices[self.all_go_branches[i][2]] = i

            for i in range(len(self.all_not_go_branches)):
                if self.all_not_go_branches[i][1] is False:
                    not_go_false_prices[self.all_not_go_branches[i][2]] = i

            if min(go_false_prices) < min(not_go_false_prices):
                min_index = go_false_prices.get(min(go_false_prices))
                m = min(go_false_prices)
            else:
                min_index = not_go_false_prices.get(min(not_go_false_prices))
                m = min(not_go_false_prices)

            if m < min_price:
                if self.is_global_go_branch:
                    if self.go_branch:
                        self.all_go_branches[-1][1] = False
                    else:
                        self.all_go_branches[-2][1] = False
                else:
                    if self.go_branch:
                        self.all_not_go_branches[-1][1] = False
                    else:
                        self.all_not_go_branches[-2][1] = False

                self.branch_jump = True

                if min(go_false_prices) < min(not_go_false_prices):
                    matrix = cp.deepcopy(self.go_matrix[min_index])
                    self.is_global_go_branch = True
                    self.all_go_branches[min_index][1] = True
                    min_price = self.all_go_branches[min_index][2]

                    if (min_index+1)%2 == 0:
                        self.go_branch = False
                        self.all_go_branches.append(self.all_go_branches[min_index])
                        self.all_go_branches.append(self.all_go_branches[min_index+1])

                        self.go_matrix.append(self.go_matrix[min_index])
                        self.go_matrix.append(self.go_matrix[min_index+1])
                    else:
                        self.go_branch = True
                        self.all_go_branches.append(self.all_go_branches[min_index-1])
                        self.all_go_branches.append(self.all_go_branches[min_index])

                        self.go_matrix.append(self.go_matrix[min_index-1])
                        self.go_matrix.append(self.go_matrix[min_index])
                else:
                    matrix = cp.deepcopy(self.not_go_matrix[min_index])
                    self.is_global_go_branch = False
                    self.all_not_go_branches[min_index][1] = True
                    min_price = self.all_not_go_branches[min_index][2]

                    if min_index == 0:
                        self.go_branch = False

                    elif (min_index+1)%2 == 0:
                        self.go_branch = False
                        self.all_not_go_branches.append(self.all_not_go_branches[min_index])
                        self.all_not_go_branches.append(self.all_not_go_branches[min_index+1])

                        self.not_go_matrix.append(self.not_go_matrix[min_index])
                        self.not_go_matrix.append(self.not_go_matrix[min_index+1])
                    else:
                        self.go_branch = True
                        self.all_not_go_branches.append(self.all_not_go_branches[min_index-1])
                        self.all_not_go_branches.append(self.all_not_go_branches[min_index])

                        self.not_go_matrix.append(self.not_go_matrix[min_index-1])
                        self.not_go_matrix.append(self.not_go_matrix[min_index])

            if len(matrix["rows"]) == 2:
                self.branch_jump = True
                self.matrix_reduction(matrix)
                row_col = []
                index = []
                print(matrix)
                if self.is_global_go_branch:
                    if self.go_branch:
                        disordered_cycle = self.all_go_branches[-1][3]
                    else:
                        disordered_cycle = self.all_go_branches[-2][3]
                    disordered_cycle.reverse()
                    disordered_cycle.append(self.all_go_branches[-1][0])

                else:
                    if self.go_branch:
                        disordered_cycle = self.all_not_go_branches[-1][3]
                    else:
                        disordered_cycle = self.all_not_go_branches[-2][3]
                    disordered_cycle.reverse()
                    disordered_cycle.append(self.all_not_go_branches[-1][0])

                row_keys = list(matrix["rows"].keys())
                row_keys.sort()
                col_keys = list(matrix["cols"].keys())
                col_keys.sort()
                for i,row in enumerate(row_keys):
                    if min(matrix["rows"][row]) == self.inf:
                        self.list_cycle_of_gamilt.addItem("Метод ветвей и границ:")
                        self.list_cycle_of_gamilt.addItem("----------------------")
                        self.list_cycle_of_gamilt.addItem("Нет цикла!")
                        return 0
                    index.append(max(matrix["rows"][row]))
                row_index = index.index(max(index))
                if matrix["rows"][row_keys[row_index]][0] < matrix["rows"][row_keys[row_index]][1]:
                    col_index = 1
                else:
                    col_index = 0

                if row_index == 0 and col_index == 0:
                    keys = list(matrix["rows"].keys())
                    matrix["rows"][keys[col_index]][row_index] = self.inf
                    matrix["rows"][keys[col_index+1]][row_index+1] = self.inf

                elif row_index == 1 and col_index == 1:
                    keys = list(matrix["rows"].keys())
                    matrix["rows"][keys[col_index-1]][row_index-1] = self.inf
                    matrix["rows"][keys[col_index]][row_index] = self.inf

                else:
                    keys = list(matrix["rows"].keys())
                    matrix["rows"][keys[row_index]][col_index] = self.inf
                    matrix["rows"][keys[col_index]][row_index] = self.inf

                for i,row in enumerate(row_keys):
                    for j,col in enumerate(col_keys):
                        if matrix["rows"][row][j] != self.inf:
                            row_col.append((row,col))

                if not row_col:
                    self.list_cycle_of_gamilt.addItem("Метод ветвей и границ:")
                    self.list_cycle_of_gamilt.addItem("----------------------")
                    self.list_cycle_of_gamilt.addItem("Нет цикла!")
                    return 0

                disordered_cycle.extend(row_col)
                print(disordered_cycle)
                print(len(disordered_cycle))
                hamilton_cycle = [disordered_cycle[0]]
                disordered_cycle.remove(disordered_cycle[0])
                i = 0
                while disordered_cycle:
                    if hamilton_cycle[-1][1] == disordered_cycle[i][0]:
                        hamilton_cycle.append(disordered_cycle[i])
                        disordered_cycle.remove(disordered_cycle[i])
                        i = 0
                    elif i == len(disordered_cycle)-1:
                        print(hamilton_cycle)
                        print(len(hamilton_cycle))
                        self.list_cycle_of_gamilt.addItem("Метод ветвей и границ:")
                        self.list_cycle_of_gamilt.addItem("----------------------")
                        self.list_cycle_of_gamilt.addItem("Нет цикла!")
                        return 0
                    else:
                        i += 1

                key = list(self.first_matrix.keys())[0]
                path_price = 0
                for edges in hamilton_cycle:
                    path_price += self.first_matrix[key]["rows"][edges[0]][edges[1]]
                end = t.time()
                alg_time = round(end - start, 5)

                self.list_cycle_of_gamilt.addItem("Метод ветвей и границ:")
                self.list_cycle_of_gamilt.addItem("----------------------")
                self.list_cycle_of_gamilt.addItem("Стоимость пути: " + str(path_price))
                self.list_cycle_of_gamilt.addItem("Гамильтонов цикл: " + str(hamilton_cycle))
                self.list_cycle_of_gamilt.addItem("Время работы: " + str(alg_time))
                self.list_cycle_of_gamilt.addItem("=============================================")

                self.clear_all()
                return 0

    def clear_all(self):
        self.go_matrix = []
        self.not_go_matrix = []
        self.go_rows_cols = []
        self.not_go_rows_cols = []
        self.is_global_go_branch = True
        self.go_branch = True
        self.first_matrix = {0: {"rows": [], "cols": []}}
        self.rows = {}
        self.cols = {}
        self.first_iteration = True
        self.second_iteration = False
        self.branch_jump = False
        self.inf = float("inf")
        self.first_node = 0
        self.all_go_branches = []
        self.all_not_go_branches = []

    def create_cycle(self, disordered_cycle):
        """ Метод собирающий цикл """
        # print("I am crush in 'create_cycle'!")
        if len(disordered_cycle) < 2:
            return False
        cycle = []
        cycle.append(disordered_cycle[-1])
        disordered_cycle.remove(disordered_cycle[-1])
        i = 0
        while disordered_cycle:
            if cycle[-1][1] == disordered_cycle[i][0]:
                # print("Цикл if ",i," : ", disordered_cycle)
                cycle.append(disordered_cycle[i])
                disordered_cycle.remove(disordered_cycle[i])
                if cycle[0][0] == cycle[-1][1]:
                    return cycle
                i = 0
            elif i == len(disordered_cycle)-1:
                # print("Цикл elif: ", disordered_cycle)
                # cycle.clear()
                # cycle.append(disordered_cycle[0])
                # disordered_cycle.remove(disordered_cycle[0])
                # try_cycle = disordered_cycle[:]
                # i = 0
                return False
            else:
                i += 1
        return False

    def subcycle_limitation(self, matrix):
        """ Метод предотвращающий оброзование подциклов"""
        # print("I am crush in 'subcycle_limitation'!")
        row_keys = list(matrix["rows"].keys())
        row_keys.sort()
        col_keys = list(matrix["cols"].keys())
        col_keys.sort()
        #Ограничения на подциклы
        for i,k in enumerate(row_keys):
            for j,col in enumerate(col_keys):
                if matrix["rows"][k][j] == 0:
                    if self.is_global_go_branch:
                        if self.go_branch:
                            disordered_subcycle = self.all_go_branches[-1][3][:]
                            disordered_subcycle.reverse()
                            disordered_subcycle.append(self.all_go_branches[-1][0])
                        else:
                            disordered_subcycle = self.all_go_branches[-2][3][:]
                            disordered_subcycle.reverse()
                    else:
                        if self.go_branch:
                            disordered_subcycle = self.all_not_go_branches[-1][3][:]
                            disordered_subcycle.reverse()
                            disordered_subcycle.append(self.all_not_go_branches[-1][0])
                        elif len(self.all_not_go_branches) < 2:
                            continue
                        else:
                            disordered_subcycle = self.all_not_go_branches[-2][3][:]
                            disordered_subcycle.reverse()

                    disordered_subcycle.append((row_keys[i], col_keys[j]))
                    if self.create_cycle(disordered_subcycle):
                        matrix["rows"][row_keys[i]][j] = self.inf
                        matrix["cols"][col_keys[j]][i] = self.inf
                        continue

    def find_cycle(self):
        inspection = self.init()
        if inspection == 0:
            return 0
        self.branch_and_bound_algorithm()