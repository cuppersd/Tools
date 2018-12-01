#  计算最短编辑距离
#  参数initialString, finalString
#  返回{'num_Insertion': num_Insertion, 'num_Deletion': num_Deletion, 'num_Substitution': num_Substitution,
#   'num_NoOp': num_NoOp, ' minimumEditDistance': minimumEditDistance}
import logging

skipNoOps = False


class Insertion:
    cost = 1

    @staticmethod
    def getDependentCellIndices(i, j):
        if i == 0 and j == 0:
            raise ArithmeticError()
        else:
            return (i, j - 1)

    @staticmethod
    def getVerb():
        return 'Insert'


class Deletion:
    cost = 1

    @staticmethod
    def getDependentCellIndices(i, j):
        if i == 0 and j == 0:
            raise ArithmeticError()
        else:
            return (i - 1, j)

    @staticmethod
    def getVerb():
        return 'Delete'


class Substitution:
    cost = 1

    def getDependentCellIndices(i, j):
        if i == 0 and j == 0:
            raise ArithmeticError()
        else:
            return (i - 1, j - 1)

    @staticmethod
    def getVerb():
        return 'Substitute'


class NoOp:
    cost = 0

    def getDependentCellIndices(i, j):
        if i == 0 and j == 0:
            raise ArithmeticError()
        else:
            return (i - 1, j - 1)

    @staticmethod
    def getVerb():
        return 'NoOp'


class Distance:
    def __init__(self, value=0):
        self.value = value
        self.operations = []

#  计算编辑距离
def computeEditDistance(initialString, finalString):
    logging.info("Calculating edit distance '{}' => '{}'".format(initialString, finalString))
    table = [[Distance(0) for j in range(0, len(finalString) + 1)]
             for i in range(0, len(initialString) + 1)
             ]
    for i in range(0, len(initialString) + 1):
        table[i][0].value = Deletion.cost * i
        if i != 0:
            table[i][0].operations.append(Deletion)

    for j in range(0, len(finalString) + 1):
        table[0][j].value = Insertion.cost * j
        if j != 0:
            table[0][j].operations.append(Insertion)

    printTable(table, initialString, finalString)

    for i in range(1, len(initialString) + 1):
        for j in range(1, len(finalString) + 1):
            initalStringIndex = i - 1
            finalStringIndex = j - 1

            costs = [(table[i][j - 1].value + Insertion.cost, Insertion),
                     (table[i - 1][j].value + Deletion.cost, Deletion),
                     (table[i - 1][j - 1].value + Substitution.cost, Substitution)
                     ]

            if initialString[initalStringIndex] == finalString[finalStringIndex]:
                costs.append((table[i - 1][j - 1].value, NoOp))

            costs.sort(key=lambda pair: pair[0])
            table[i][j].value = costs[0][0]

            minimumCost = costs[0][0]
            for (costValue, costType) in costs:
                if costValue > minimumCost:
                    break

                table[i][j].operations.append(costType)
    printTable(table, initialString, finalString)
    return table


def printTable(table, initialString, finalString):
    m = len(table)
    n = len(table[0])

    row_format = "{:^5}" * (len(finalString) + 2)
    header = list("  ")
    header.extend(finalString)
    for rowNum in range(0, len(initialString) + 1):
        row = []
        if rowNum == 0:
            row.append(' ')
        else:
            row.append(initialString[rowNum - 1])

        row += [ed.value for ed in table[rowNum]]


def computeOperations(table, initialString, finalString, recordNoOps):
    from collections import namedtuple
    import copy
    Operation = namedtuple('Operation', ['point', 'op'])
    incomplete_solutions = []
    complete_solutions = []

    i = len(initialString)
    j = len(finalString)
    d = table[i][j]
    for op in d.operations:
        incomplete_solutions.append([Operation(point=(i, j), op=op)])
    while len(incomplete_solutions) > 0:
        solution = incomplete_solutions.pop()
        current = solution[-1]
        i = current.point[0]
        j = current.point[1]
        while not (i == 0 and j == 0):
            new_location = current.op.getDependentCellIndices(i, j)
            i = new_location[0]
            j = new_location[1]

            nextCell = table[i][j]
            numberOfOperationsAdded = 0
            for op in nextCell.operations:
                newOperation = Operation(point=(i, j), op=op)

                if op == NoOp and not recordNoOps:
                    current = newOperation
                    continue

                if numberOfOperationsAdded == 0:
                    current = newOperation
                    solution.append(newOperation)
                else:
                    newSolution = copy.deepcopy(solution)
                    newSolution.append(newOperation)
                    incomplete_solutions.append(newSolution)

                numberOfOperationsAdded += 1
        solution.reverse()
        complete_solutions.append(solution)
    return complete_solutions


def printSolution(solution, initialString, finalString, minimumEditDistance):
    num_Insertion = 0
    num_Deletion = 0
    num_Substitution = 0
    num_NoOp = 0
    for op in solution:
        msg = op.op.getVerb() + " "
        if op.op == Insertion:
            msg += "'{}'".format(finalString[op.point[1] - 1])
            num_Insertion = num_Insertion + 1
        elif op.op == Deletion:
            msg += "'{}'".format(initialString[op.point[0] - 1])
            num_Deletion = num_Deletion + 1
        elif op.op == Substitution:
            msg += "'{}' for '{}'".format(initialString[op.point[0] - 1],
                                          finalString[op.point[1] - 1])
            num_Substitution = num_Substitution + 1
        elif op.op == NoOp:
            msg += "'{}' = '{}'".format(initialString[op.point[0] - 1],
                                        finalString[op.point[1] - 1])
            num_NoOp = num_NoOp + 1

        else:
            raise Exception('Unsupported op')

        print(msg)
    result_dict = {'num_Insertion': num_Insertion, 'num_Deletion': num_Deletion, 'num_Substitution': num_Substitution,
                   'num_NoOp': num_NoOp, ' minimumEditDistance': minimumEditDistance}
    return result_dict


def main(initialString, finalString):
    ed = computeEditDistance(initialString, finalString)  # 调用字符串匹配算法
    minimumEditDistance = ed[len(initialString)][len(finalString)].value  #
    logging.info("Minimum edit distance is {}".format(minimumEditDistance))
    solutions = computeOperations(ed, initialString, finalString, '--record_noops')
    for (index, s) in enumerate([solutions[0]]):  # 打印编辑距离
        return printSolution(s, initialString, finalString, minimumEditDistance)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # 日志信息
    initialString = "ZHANG"  # 初始的字符串
    finalString = "ZHJIE"  # 最终字符串
    print(main(initialString, finalString))
