import sys
from find_probability import *
from expected_utility import *
from algo import *

nodeList = []
decisionNodeList = []
queryList = []
executeQuery = []
lines = []


def get_values(lines_args):
    line_copy = lines_args
    f = False
    k = 0
    for line in line_copy:
        k += 1
        line = line.strip().split()
        if '******' in line or f:
            probFunction(line_copy, k)
            break
    line_copy = lines_args
    for line in line_copy:
        line = line.strip()
        if '******' in line:
            break
        else:
            full_query_list = line
            query_type = full_query_list.split('(')
            query_type_1 = query_type[1].replace(')', '')
            queryList.append([query_type[0]] + [query_type_1])


def read_input(input_file):
    global lines
    f = open(input_file, 'r')
    lines = f.readlines()
    get_values(lines)


def probFunction(lines_copy, k):
    while k < len(lines_copy):
        if '|' not in lines_copy[k]:
            node_name = str(lines_copy[k].strip())
            next_element = lines_copy[k + 1].strip()
            if next_element == 'decision':
                true_value = 0.5
                false_value = 0.5
                nodeList.append(DiscreteBayesNode(node_name, [], DiscreteCPT(['T', 'F'], [true_value, false_value])))
                decisionNodeList.append(
                    DiscreteBayesNode(node_name, [], DiscreteCPT(['T', 'F'], [true_value, false_value])))
                k += 3
            else:
                true_value = float((lines_copy[k + 1]).split()[0])
                false_value = 1 - true_value
                nodeList.append(DiscreteBayesNode(node_name, [], DiscreteCPT(['T', 'F'], [true_value, false_value])))
                k += 3
        elif '|' in lines_copy[k]:
            parents_list = []
            temporary_node = (lines_copy[k]).strip().split('|')
            node_name = str(temporary_node[0].strip())
            num_parents = len(temporary_node[1].lstrip().rstrip().split())
            parents_list.append(temporary_node[1].lstrip().rstrip().split())
            if num_parents == 1:
                true_value = [0] * 2
                false_value = [0] * 2
                line = []
                for i in range(0, 2):
                    line.append(lines[k + i + 1])
                truth_table_1 = line[0].split()
                truth_table_2 = line[1].split()
                if truth_table_1[1] == '+':
                    true_value[0] = float(truth_table_1[0])
                    false_value[0] = 1 - float(true_value[0])
                    true_value[1] = float(truth_table_2[0])
                    false_value[1] = 1 - float((true_value[1]))
                else:
                    true_value[1] = float(truth_table_1[0])
                    false_value[1] = 1 - float(true_value[1])
                    true_value[0] = float(truth_table_2[0])
                    false_value[0] = 1 - float(true_value[0])
                nodeList.append(DiscreteBayesNode(node_name, parents_list[0], DiscreteCPT(['T', 'F'],
                                                                                          {('T',): [true_value[0],
                                                                                                    false_value[0]],
                                                                                           ('F',): [true_value[1],
                                                                                                    false_value[1]]})))
                k += 4
            elif num_parents == 2:
                true_value = [0] * 4
                false_value = [0] * 4
                line = []
                for i in range(0, 4):
                    line.append(lines[k + i + 1])
                truth_table_1 = line[0].split()
                truth_table_2 = line[1].split()
                truth_table_3 = line[2].split()
                truth_table_4 = line[3].split()
                if truth_table_1[1] == '+' and truth_table_1[2] == '+':
                    true_value[0] = float(truth_table_1[0])
                    false_value[0] = 1 - float(true_value[0])
                elif truth_table_1[1] == '+' and truth_table_1[2] == '-':
                    true_value[1] = float(truth_table_1[0])
                    false_value[1] = 1 - float(true_value[1])
                elif truth_table_1[1] == '-' and truth_table_1[2] == '+':
                    true_value[2] = float(truth_table_1[0])
                    false_value[2] = 1 - float(true_value[2])
                elif truth_table_1[1] == '-' and truth_table_1[2] == '-':
                    true_value[3] = float(truth_table_1[0])
                    false_value[3] = 1 - float(true_value[3])

                if truth_table_2[1] == '+' and truth_table_2[2] == '+':
                    true_value[0] = float(truth_table_2[0])
                    false_value[0] = 1 - float(true_value[0])
                elif truth_table_2[1] == '+' and truth_table_2[2] == '-':
                    true_value[1] = float(truth_table_2[0])
                    false_value[1] = 1 - float(true_value[1])
                elif truth_table_2[1] == '-' and truth_table_2[2] == '+':
                    true_value[2] = float(truth_table_2[0])
                    false_value[2] = 1 - float(true_value[2])
                elif truth_table_2[1] == '-' and truth_table_2[2] == '-':
                    true_value[3] = float(truth_table_2[0])
                    false_value[3] = 1 - float(true_value[3])

                if truth_table_3[1] == '+' and truth_table_3[2] == '+':
                    true_value[0] = float(truth_table_3[0])
                    false_value[0] = 1 - float(true_value[0])
                elif truth_table_3[1] == '+' and truth_table_3[2] == '-':
                    true_value[1] = float(truth_table_3[0])
                    false_value[1] = 1 - float(true_value[1])
                elif truth_table_3[1] == '-' and truth_table_3[2] == '+':
                    true_value[2] = float(truth_table_3[0])
                    false_value[2] = 1 - float(true_value[2])
                elif truth_table_3[1] == '-' and truth_table_3[2] == '-':
                    true_value[3] = float(truth_table_3[0])
                    false_value[3] = 1 - float(true_value[3])

                if truth_table_4[1] == '+' and truth_table_4[2] == '+':
                    true_value[0] = float(truth_table_4[0])
                    false_value[0] = 1 - float(true_value[0])
                elif truth_table_4[1] == '+' and truth_table_4[2] == '-':
                    true_value[1] = float(truth_table_4[0])
                    false_value[1] = 1 - float(true_value[1])
                elif truth_table_4[1] == '-' and truth_table_4[2] == '+':
                    true_value[2] = float(truth_table_4[0])
                    false_value[2] = 1 - float(true_value[2])
                elif truth_table_4[1] == '-' and truth_table_4[2] == '-':
                    true_value[3] = float(truth_table_4[0])
                    false_value[3] = 1 - float(true_value[3])

                nodeList.append(
                    DiscreteBayesNode(node_name, [parents_list[0][0], parents_list[0][1]], DiscreteCPT(['T', 'F'],
                                                                                                       {('T', 'T'): [
                                                                                                           true_value[
                                                                                                               0],
                                                                                                           false_value[
                                                                                                               0]],
                                                                                                           ('T', 'F'): [
                                                                                                               true_value[
                                                                                                                   1],
                                                                                                               false_value[
                                                                                                                   1]],
                                                                                                           ('F', 'T'): [
                                                                                                               true_value[
                                                                                                                   2],
                                                                                                               false_value[
                                                                                                                   2]],
                                                                                                           ('F', 'F'): [
                                                                                                               true_value[
                                                                                                                   3],
                                                                                                               false_value[
                                                                                                                   3]]})))
                k += 6

            elif num_parents == 3:
                true_value = [0] * 8
                false_value = [0] * 8
                line = []
                for i in range(0, 8):
                    line.append(lines[k + i + 1])
                truth_table_1 = line[0].split()
                truth_table_2 = line[1].split()
                truth_table_3 = line[2].split()
                truth_table_4 = line[3].split()
                truth_table_5 = line[4].split()
                truth_table_6 = line[5].split()
                truth_table_7 = line[6].split()
                truth_table_8 = line[7].split()
                if truth_table_1[1] == '+' and truth_table_1[2] == '+' and truth_table_1[3] == '+':
                    true_value[0] = float(truth_table_1[0])
                    false_value[0] = 1 - float(true_value[0])
                elif truth_table_1[1] == '+' and truth_table_1[2] == '+' and truth_table_1[3] == '-':
                    true_value[1] = float(truth_table_1[0])
                    false_value[1] = 1 - float(true_value[1])
                elif truth_table_1[1] == '+' and truth_table_1[2] == '-' and truth_table_1[3] == '+':
                    true_value[2] = float(truth_table_1[0])
                    false_value[2] = 1 - float(true_value[2])
                elif truth_table_1[1] == '+' and truth_table_1[2] == '-' and truth_table_1[3] == '-':
                    true_value[3] = float(truth_table_1[0])
                    false_value[3] = 1 - float(true_value[3])
                elif truth_table_1[1] == '-' and truth_table_1[2] == '+' and truth_table_1[3] == '+':
                    true_value[4] = float(truth_table_1[0])
                    false_value[4] = 1 - float(true_value[4])
                elif truth_table_1[1] == '-' and truth_table_1[2] == '+' and truth_table_1[3] == '-':
                    true_value[5] = float(truth_table_1[0])
                    false_value[5] = 1 - float(true_value[5])
                elif truth_table_1[1] == '-' and truth_table_1[2] == '-' and truth_table_1[3] == '+':
                    true_value[6] = float(truth_table_1[0])
                    false_value[6] = 1 - float(true_value[6])
                elif truth_table_1[1] == '-' and truth_table_1[2] == '-' and truth_table_1[3] == '-':
                    true_value[7] = float(truth_table_1[0])
                    false_value[7] = 1 - float(true_value[7])

                if truth_table_2[1] == '+' and truth_table_2[2] == '+' and truth_table_2[3] == '+':
                    true_value[0] = float(truth_table_2[0])
                    false_value[0] = 1 - float(true_value[0])
                elif truth_table_2[1] == '+' and truth_table_2[2] == '+' and truth_table_2[3] == '-':
                    true_value[1] = float(truth_table_2[0])
                    false_value[1] = 1 - float(true_value[1])
                elif truth_table_2[1] == '+' and truth_table_2[2] == '-' and truth_table_2[3] == '+':
                    true_value[2] = float(truth_table_2[0])
                    false_value[2] = 1 - float(true_value[2])
                elif truth_table_2[1] == '+' and truth_table_2[2] == '-' and truth_table_2[3] == '-':
                    true_value[3] = float(truth_table_2[0])
                    false_value[3] = 1 - float(true_value[3])
                elif truth_table_2[1] == '-' and truth_table_2[2] == '+' and truth_table_2[3] == '+':
                    true_value[4] = float(truth_table_2[0])
                    false_value[4] = 1 - float(true_value[4])
                elif truth_table_2[1] == '-' and truth_table_2[2] == '+' and truth_table_2[3] == '-':
                    true_value[5] = float(truth_table_2[0])
                    false_value[5] = 1 - float(true_value[5])
                elif truth_table_2[1] == '-' and truth_table_2[2] == '-' and truth_table_2[3] == '+':
                    true_value[6] = float(truth_table_2[0])
                    false_value[6] = 1 - float(true_value[6])
                elif truth_table_2[1] == '-' and truth_table_2[2] == '-' and truth_table_2[3] == '-':
                    true_value[7] = float(truth_table_2[0])
                    false_value[7] = 1 - float(true_value[7])

                if truth_table_3[1] == '+' and truth_table_3[2] == '+' and truth_table_3[3] == '+':
                    true_value[0] = float(truth_table_3[0])
                    false_value[0] = 1 - float(true_value[0])
                elif truth_table_3[1] == '+' and truth_table_3[2] == '+' and truth_table_3[3] == '-':
                    true_value[1] = float(truth_table_3[0])
                    false_value[1] = 1 - float(true_value[1])
                elif truth_table_3[1] == '+' and truth_table_3[2] == '-' and truth_table_3[3] == '+':
                    true_value[2] = float(truth_table_3[0])
                    false_value[2] = 1 - float(true_value[2])
                elif truth_table_3[1] == '+' and truth_table_3[2] == '-' and truth_table_3[3] == '-':
                    true_value[3] = float(truth_table_3[0])
                    false_value[3] = 1 - float(true_value[3])
                elif truth_table_3[1] == '-' and truth_table_3[2] == '+' and truth_table_3[3] == '+':
                    true_value[4] = float(truth_table_3[0])
                    false_value[4] = 1 - float(true_value[4])
                elif truth_table_3[1] == '-' and truth_table_3[2] == '+' and truth_table_3[3] == '-':
                    true_value[5] = float(truth_table_3[0])
                    false_value[5] = 1 - float(true_value[5])
                elif truth_table_3[1] == '-' and truth_table_3[2] == '-' and truth_table_3[3] == '+':
                    true_value[6] = float(truth_table_3[0])
                    false_value[6] = 1 - float(true_value[6])
                elif truth_table_3[1] == '-' and truth_table_3[2] == '-' and truth_table_3[3] == '-':
                    true_value[7] = float(truth_table_3[0])
                    false_value[7] = 1 - float(true_value[7])

                if truth_table_4[1] == '+' and truth_table_4[2] == '+' and truth_table_4[3] == '+':
                    true_value[0] = float(truth_table_4[0])
                    false_value[0] = 1 - float(true_value[0])
                elif truth_table_4[1] == '+' and truth_table_4[2] == '+' and truth_table_4[3] == '-':
                    true_value[1] = float(truth_table_4[0])
                    false_value[1] = 1 - float(true_value[1])
                elif truth_table_4[1] == '+' and truth_table_4[2] == '-' and truth_table_4[3] == '+':
                    true_value[2] = float(truth_table_4[0])
                    false_value[2] = 1 - float(true_value[2])
                elif truth_table_4[1] == '+' and truth_table_4[2] == '-' and truth_table_4[3] == '-':
                    true_value[3] = float(truth_table_4[0])
                    false_value[3] = 1 - float(true_value[3])
                elif truth_table_4[1] == '-' and truth_table_4[2] == '+' and truth_table_4[3] == '+':
                    true_value[4] = float(truth_table_4[0])
                    false_value[4] = 1 - float(true_value[4])
                elif truth_table_4[1] == '-' and truth_table_4[2] == '+' and truth_table_4[3] == '-':
                    true_value[5] = float(truth_table_4[0])
                    false_value[5] = 1 - float(true_value[5])
                elif truth_table_4[1] == '-' and truth_table_4[2] == '-' and truth_table_4[3] == '+':
                    true_value[6] = float(truth_table_4[0])
                    false_value[6] = 1 - float(true_value[6])
                elif truth_table_4[1] == '-' and truth_table_4[2] == '-' and truth_table_4[3] == '-':
                    true_value[7] = float(truth_table_4[0])
                    false_value[7] = 1 - float(true_value[7])

                if truth_table_5[1] == '+' and truth_table_5[2] == '+' and truth_table_5[3] == '+':
                    true_value[0] = float(truth_table_5[0])
                    false_value[0] = 1 - float(true_value[0])
                elif truth_table_5[1] == '+' and truth_table_5[2] == '+' and truth_table_5[3] == '-':
                    true_value[1] = float(truth_table_5[0])
                    false_value[1] = 1 - float(true_value[1])
                elif truth_table_5[1] == '+' and truth_table_5[2] == '-' and truth_table_5[3] == '+':
                    true_value[2] = float(truth_table_5[0])
                    false_value[2] = 1 - float(true_value[2])
                elif truth_table_5[1] == '+' and truth_table_5[2] == '-' and truth_table_5[3] == '-':
                    true_value[3] = float(truth_table_5[0])
                    false_value[3] = 1 - float(true_value[3])
                elif truth_table_5[1] == '-' and truth_table_5[2] == '+' and truth_table_5[3] == '+':
                    true_value[4] = float(truth_table_5[0])
                    false_value[4] = 1 - float(true_value[4])
                elif truth_table_5[1] == '-' and truth_table_5[2] == '+' and truth_table_5[3] == '-':
                    true_value[5] = float(truth_table_5[0])
                    false_value[5] = 1 - float(true_value[5])
                elif truth_table_5[1] == '-' and truth_table_5[2] == '-' and truth_table_5[3] == '+':
                    true_value[6] = float(truth_table_5[0])
                    false_value[6] = 1 - float(true_value[6])
                elif truth_table_5[1] == '-' and truth_table_5[2] == '-' and truth_table_5[3] == '-':
                    true_value[7] = float(truth_table_5[0])
                    false_value[7] = 1 - float(true_value[7])

                if truth_table_6[1] == '+' and truth_table_6[2] == '+' and truth_table_6[3] == '+':
                    true_value[0] = float(truth_table_6[0])
                    false_value[0] = 1 - float(true_value[0])
                elif truth_table_6[1] == '+' and truth_table_6[2] == '+' and truth_table_6[3] == '-':
                    true_value[1] = float(truth_table_6[0])
                    false_value[1] = 1 - float(true_value[1])
                elif truth_table_6[1] == '+' and truth_table_6[2] == '-' and truth_table_6[3] == '+':
                    true_value[2] = float(truth_table_6[0])
                    false_value[2] = 1 - float(true_value[2])
                elif truth_table_6[1] == '+' and truth_table_6[2] == '-' and truth_table_6[3] == '-':
                    true_value[3] = float(truth_table_6[0])
                    false_value[3] = 1 - float(true_value[3])
                elif truth_table_6[1] == '-' and truth_table_6[2] == '+' and truth_table_6[3] == '+':
                    true_value[4] = float(truth_table_6[0])
                    false_value[4] = 1 - float(true_value[4])
                elif truth_table_6[1] == '-' and truth_table_6[2] == '+' and truth_table_6[3] == '-':
                    true_value[5] = float(truth_table_6[0])
                    false_value[5] = 1 - float(true_value[5])
                elif truth_table_6[1] == '-' and truth_table_6[2] == '-' and truth_table_6[3] == '+':
                    true_value[6] = float(truth_table_6[0])
                    false_value[6] = 1 - float(true_value[6])
                elif truth_table_6[1] == '-' and truth_table_6[2] == '-' and truth_table_6[3] == '-':
                    true_value[7] = float(truth_table_6[0])
                    false_value[7] = 1 - float(true_value[7])

                if truth_table_7[1] == '+' and truth_table_7[2] == '+' and truth_table_7[3] == '+':
                    true_value[0] = float(truth_table_7[0])
                    false_value[0] = 1 - float(true_value[0])
                elif truth_table_7[1] == '+' and truth_table_7[2] == '+' and truth_table_7[3] == '-':
                    true_value[1] = float(truth_table_7[0])
                    false_value[1] = 1 - float(true_value[1])
                elif truth_table_7[1] == '+' and truth_table_7[2] == '-' and truth_table_7[3] == '+':
                    true_value[2] = float(truth_table_7[0])
                    false_value[2] = 1 - float(true_value[2])
                elif truth_table_7[1] == '+' and truth_table_7[2] == '-' and truth_table_7[3] == '-':
                    true_value[3] = float(truth_table_7[0])
                    false_value[3] = 1 - float(true_value[3])
                elif truth_table_7[1] == '-' and truth_table_7[2] == '+' and truth_table_7[3] == '+':
                    true_value[4] = float(truth_table_7[0])
                    false_value[4] = 1 - float(true_value[4])
                elif truth_table_7[1] == '-' and truth_table_7[2] == '+' and truth_table_7[3] == '-':
                    true_value[5] = float(truth_table_7[0])
                    false_value[5] = 1 - float(true_value[5])
                elif truth_table_7[1] == '-' and truth_table_7[2] == '-' and truth_table_7[3] == '+':
                    true_value[6] = float(truth_table_7[0])
                    false_value[6] = 1 - float(true_value[6])
                elif truth_table_7[1] == '-' and truth_table_7[2] == '-' and truth_table_7[3] == '-':
                    true_value[7] = float(truth_table_7[0])
                    false_value[7] = 1 - float(true_value[7])

                if truth_table_8[1] == '+' and truth_table_8[2] == '+' and truth_table_8[3] == '+':
                    true_value[0] = float(truth_table_8[0])
                    false_value[0] = 1 - float(true_value[0])
                elif truth_table_8[1] == '+' and truth_table_8[2] == '+' and truth_table_8[3] == '-':
                    true_value[1] = float(truth_table_8[0])
                    false_value[1] = 1 - float(true_value[1])
                elif truth_table_8[1] == '+' and truth_table_8[2] == '-' and truth_table_8[3] == '+':
                    true_value[2] = float(truth_table_8[0])
                    false_value[2] = 1 - float(true_value[2])
                elif truth_table_8[1] == '+' and truth_table_8[2] == '-' and truth_table_8[3] == '-':
                    true_value[3] = float(truth_table_8[0])
                    false_value[3] = 1 - float(true_value[3])
                elif truth_table_8[1] == '-' and truth_table_8[2] == '+' and truth_table_8[3] == '+':
                    true_value[4] = float(truth_table_8[0])
                    false_value[4] = 1 - float(true_value[4])
                elif truth_table_8[1] == '-' and truth_table_8[2] == '+' and truth_table_8[3] == '-':
                    true_value[5] = float(truth_table_8[0])
                    false_value[5] = 1 - float(true_value[5])
                elif truth_table_8[1] == '-' and truth_table_8[2] == '-' and truth_table_8[3] == '+':
                    true_value[6] = float(truth_table_8[0])
                    false_value[6] = 1 - float(true_value[6])
                elif truth_table_8[1] == '-' and truth_table_8[2] == '-' and truth_table_8[3] == '-':
                    true_value[7] = float(truth_table_8[0])
                    false_value[7] = 1 - float(true_value[7])

                nodeList.append(
                    DiscreteBayesNode(node_name, [parents_list[0][0], parents_list[0][1], parents_list[0][2]],
                                      DiscreteCPT(['T', 'F'],
                                                  {('T', 'T', 'T'): [true_value[0], false_value[0]],
                                                   ('T', 'T', 'F'): [true_value[1], false_value[1]],
                                                   ('T', 'F', 'T'): [true_value[2], false_value[2]],
                                                   ('T', 'F', 'F'): [true_value[3], false_value[3]],
                                                   ('F', 'T', 'T'): [true_value[4], false_value[4]],
                                                   ('F', 'T', 'F'): [true_value[5], false_value[5]],
                                                   ('F', 'F', 'T'): [true_value[6], false_value[6]],
                                                   ('F', 'F', 'F'): [true_value[7], false_value[7]]})))
                k += 10


def execQuery():
    overall_query = []
    for query in queryList:
        actual_arg = []

        if query[0] == 'P' or query[0] == 'EU':
            query_type = query[0]
            if '|' in query[1]:
                fpart = []
                temporary_args = query[1].split('|')
                ftempart = []
                temporary_args[0] = temporary_args[0].strip()
                temporary_tt = temporary_args[0].split(',')
                for i in temporary_tt:
                    temporary_t = i.split('=')
                    ftempart.append(temporary_t[0].strip())
                    if temporary_t[1].strip() == '+':
                        ftempart.append('T')
                    elif temporary_t[1].strip() == '-':
                        ftempart.append('F')
                fpart.append(ftempart + ['|'])
                argc = temporary_args[1].split(',')
                for temporary in argc:
                    temporary = temporary.strip()
                    param = temporary.split('=')
                    var = param[0].strip()
                    val = param[1].strip()
                    if val == '+':
                        actual_arg.append([var] + ['T'])
                    else:
                        actual_arg.append([var] + ['F'])
                overall_query.append([query_type] + fpart + actual_arg)
            else:
                args = query[1].split(',')
                for temporary in args:
                    temporary = temporary.strip()
                    param = temporary.split('=')
                    var = param[0].strip()
                    val = param[1].strip()
                    if val == '+':
                        actual_arg.append([var] + ['T'])
                    else:
                        actual_arg.append([var] + ['F'])
                overall_query.append([query_type] + actual_arg)

        elif query[0] == 'MEU':
            query_type = query[0]
            if '|' in query[1]:
                fpart = []
                temporary_args = query[1].split('|')
                ftempart = []
                temporary_args[0] = temporary_args[0].strip()
                temporary_tt = temporary_args[0].split(',')
                for i in temporary_tt:
                    if '=' in i:
                        temporary_t = i.split('=')
                        ftempart.append(temporary_t[0].strip())
                        if temporary_t[1].strip() == '+':
                            ftempart.append('T')
                        elif temporary_t[1].strip() == '-':
                            ftempart.append('F')
                        else:
                            ftempart.append('*')
                    else:
                        ftempart.append(i)
                        ftempart.append('*')
                fpart.append(ftempart + ['|'])
                argc = temporary_args[1].split(',')
                for temporary in argc:
                    temporary = temporary.strip()
                    if '=' in temporary:
                        param = temporary.split('=')
                        var = param[0].strip()
                        val = param[1].strip()
                        if val == '+':
                            actual_arg.append([var] + ['T'])
                        else:
                            actual_arg.append([var] + ['F'])
                    else:
                        param = temporary.split('=')
                        var = param[0].strip()
                        actual_arg.append([var] + ['*'])
                overall_query.append([query_type] + fpart + actual_arg)
            else:
                args = query[1].split(',')
                for temporary in args:
                    temporary = temporary.strip()
                    if '=' in temporary:
                        param = temporary.split('=')
                        var = param[0].strip()
                        val = param[1].strip()
                        if val == '+':
                            actual_arg.append([var] + ['T'])
                        else:
                            actual_arg.append([var] + ['F'])
                    else:
                        param = temporary.split('=')
                        var = param[0].strip()
                        actual_arg.append([var] + ['*'])
                overall_query.append([query_type] + actual_arg)
    executeQuery.append(overall_query)


file_name = sys.argv[2]
read_input(file_name)
output_file = open("output.txt", "w")
bayes_output_network = DiscreteBayesNet(nodeList)
execQuery()
counter_new_line = len(queryList)
for queries in executeQuery[0]:
    counter_new_line -= 1
    if queries[0] == 'P':
        i = calculate_probability(queries, bayes_output_network)
        output_file.write(str(i))

    if queries[0] == 'EU':
        i = expected_utility(queries, bayes_output_network, nodeList, decisionNodeList)
        output_file.write(str(i))

    if queries[0] == 'MEU':
        no_meu_queries = len(queries) - 1
        query_truth = []
        query_false = []
        query_truth.append('EU')
        query_false.append('EU')
        starQueries = 0
        starQueryList = []
        notStarQueryList = []
        for i in range(1, len(queries)):
            if queries[i][1] == '*':
                starQueries += 1
                starQueryList.append(queries[i][0])
            else:
                notStarQueryList.append([queries[i][0]] + [queries[i][1]])

        if starQueries == 1:
            outputList = [0] * 2
            for i in starQueryList:
                query_truth.append([i] + ['T'])
                query_false.append([i] + ['F'])
            for i in notStarQueryList:
                query_truth.append(i)
                query_false.append(i)
            t1 = expected_utility(query_truth, bayes_output_network, nodeList, decisionNodeList)
            t2 = expected_utility(query_false, bayes_output_network, nodeList, decisionNodeList)
            outputList.append(t1)
            outputList.append(t2)
            if t1 > t2:
                output_file.write("+ " + str(t1))
            else:
                output_file.write("- " + str(t2))

        if starQueries == 2:
            outputList = [0] * 4
            for i in starQueryList:
                query_truth.append([i] + ['T'])
                query_false.append([i] + ['F'])
            for i in notStarQueryList:
                query_truth.append(i)
                query_false.append(i)
            # TT FF
            t1 = expected_utility(query_truth, bayes_output_network, nodeList, decisionNodeList)
            t4 = expected_utility(query_false, bayes_output_network, nodeList, decisionNodeList)
            query_truth[1][1] = 'F'
            # FT
            t3 = expected_utility(query_truth, bayes_output_network, nodeList, decisionNodeList)
            query_false[1][1] = 'T'
            # TF
            t2 = expected_utility(query_false, bayes_output_network, nodeList, decisionNodeList)
            outputList.append(t1)
            outputList.append(t2)
            outputList.append(t3)
            outputList.append(t4)
            temp = max(outputList)
            if temp == t1:
                output_file.write("+ + " + str(t1))
            elif temp == t2:
                output_file.write("+ - " + str(t2))
            elif temp == t3:
                output_file.write("- + " + str(t3))
            elif temp == t4:
                output_file.write("- - " + str(t4))

        if starQueries == 3:
            outputList = [0] * 8
            for i in starQueryList:
                query_truth.append([i] + ['T'])
                query_false.append([i] + ['F'])
            for i in notStarQueryList:
                query_truth.append(i)
                query_false.append(i)
            # TTT FFF
            t1 = expected_utility(query_truth, bayes_output_network, nodeList, decisionNodeList)
            t8 = expected_utility(query_false, bayes_output_network, nodeList, decisionNodeList)
            query_truth[3][1] = 'F'
            # TTF
            t2 = expected_utility(query_truth, bayes_output_network, nodeList, decisionNodeList)
            query_truth[2][1] = 'F'
            # TFF
            t4 = expected_utility(query_truth, bayes_output_network, nodeList, decisionNodeList)
            query_truth[3][1] = 'T'
            # TFT
            t3 = expected_utility(query_truth, bayes_output_network, nodeList, decisionNodeList)
            query_false[2][1] = 'T'
            # FTF
            t6 = expected_utility(query_false, bayes_output_network, nodeList, decisionNodeList)
            query_false[3][1] = 'T'
            # FTT
            t5 = expected_utility(query_false, bayes_output_network, nodeList, decisionNodeList)
            query_false[2][1] = 'F'
            # FFT
            t7 = expected_utility(query_false, bayes_output_network, nodeList, decisionNodeList)
            outputList.append(t1)
            outputList.append(t2)
            outputList.append(t3)
            outputList.append(t4)
            outputList.append(t5)
            outputList.append(t6)
            outputList.append(t7)
            outputList.append(t8)
            temp = max(outputList)
            if temp == t1:
                output_file.write("+ + + " + str(t1))
            elif temp == t2:
                output_file.write("+ + - " + str(t2))
            elif temp == t3:
                output_file.write("+ - + " + str(t3))
            elif temp == t4:
                output_file.write("+ - - " + str(t4))
            elif temp == t5:
                output_file.write("- + + " + str(t5))
            elif temp == t6:
                output_file.write("- + - " + str(t6))
            elif temp == t7:
                output_file.write("- - + " + str(t7))
            elif temp == t8:
                output_file.write("- - - " + str(t8))
    if counter_new_line > 0:
        output_file.write("\n")