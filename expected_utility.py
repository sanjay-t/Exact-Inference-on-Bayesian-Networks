import copy


def expected_utility(queries, bayes_output_network, node_list, decision_node_list):
    evidence = dict()
    if '|' in queries[1]:
        if len(queries[1]) > 3:
            evidence = dict()
            for i in range(1, len(queries)):
                if len(queries[i]) > 3:
                    count = 0
                    while count < (len(queries[i]) - 1):
                        evidence[queries[i][count]] = queries[i][count + 1]
                        count += 2
                evidence[queries[i][0]] = queries[i][1]
        else:
            for i in range(1, len(queries)):
                evidence[queries[i][0]] = queries[i][1]
    else:
        for i in range(1, len(queries)):
            evidence[queries[i][0]] = queries[i][1]
    utility_parents = node_list[len(node_list) - 1].parents
    no_decision_nodes = 0
    utility_parents_decision_nodes = []
    utility_parent_evidence = dict()
    utility_parents_not_decision = copy.deepcopy(utility_parents)
    for i in decision_node_list:
        if i.name in utility_parents:
            utility_parents_not_decision.remove(i.name)
    for i in utility_parents:
        for j in decision_node_list:
            if i == j.name:
                no_decision_nodes += 1
                utility_parents_decision_nodes.append(i)
    for i in utility_parents_decision_nodes:
        f = True
        for q in queries:
            if i in q[0]:
                f = False
                index = q[1]
            if f:
                utility_parent_evidence[i] = 'T'
            else:
                utility_parent_evidence[i] = index

    if len(utility_parents_not_decision) == 1:
        decision_true = bayes_output_network.enumerate_ask(utility_parents[0], evidence)['T']
        decision_false = bayes_output_network.enumerate_ask(utility_parents[0], evidence)['F']
        utility_parent_evidence[utility_parents_not_decision[0]] = 'T'
        utility_output_1 = decision_true * \
                           (bayes_output_network.enumerate_ask('utility', utility_parent_evidence))['T']
        utility_parent_evidence[utility_parents_not_decision[0]] = 'F'
        utility_output_2 = decision_false * \
                           (bayes_output_network.enumerate_ask('utility', utility_parent_evidence))['T']
        return int(round((utility_output_1 + utility_output_2) + (1e-8)))

    if len(utility_parents_not_decision) == 2:
        utility_parents_copy = copy.deepcopy(utility_parents_not_decision)
        evidence_copy = copy.deepcopy(evidence)
        evidence_copy[utility_parents_copy[0]] = 'T'
        evidence_copy[utility_parents_copy[1]] = 'T'
        temporary_output1 = bayes_output_network.prob(evidence_copy)
        temporary_output2 = bayes_output_network.prob(evidence)
        final_output_from_temp = temporary_output1 / temporary_output2
        utility_parent_evidence[utility_parents_not_decision[0]] = 'T'
        utility_parent_evidence[utility_parents_not_decision[1]] = 'T'
        utility_output_1 = final_output_from_temp * \
                           (bayes_output_network.enumerate_ask('utility', utility_parent_evidence))['T']

        utility_parents_copy = copy.deepcopy(utility_parents_not_decision)
        evidence_copy = copy.deepcopy(evidence)
        evidence_copy[utility_parents_copy[0]] = 'T'
        evidence_copy[utility_parents_copy[1]] = 'F'
        temporary_output1 = bayes_output_network.prob(evidence_copy)
        temporary_output2 = bayes_output_network.prob(evidence)
        final_output_from_temp = temporary_output1 / temporary_output2
        utility_parent_evidence[utility_parents_not_decision[0]] = 'T'
        utility_parent_evidence[utility_parents_not_decision[1]] = 'F'
        utility_output_2 = final_output_from_temp * \
                           (bayes_output_network.enumerate_ask('utility', utility_parent_evidence))['T']

        utility_parents_copy = copy.deepcopy(utility_parents_not_decision)
        evidence_copy = copy.deepcopy(evidence)
        evidence_copy[utility_parents_copy[0]] = 'F'
        evidence_copy[utility_parents_copy[1]] = 'T'
        temporary_output1 = bayes_output_network.prob(evidence_copy)
        temporary_output2 = bayes_output_network.prob(evidence)
        final_output_from_temp = temporary_output1 / temporary_output2
        utility_parent_evidence[utility_parents_not_decision[0]] = 'F'
        utility_parent_evidence[utility_parents_not_decision[1]] = 'T'
        utility_output_3 = final_output_from_temp * \
                           (bayes_output_network.enumerate_ask('utility', utility_parent_evidence))['T']

        utility_parents_copy = copy.deepcopy(utility_parents_not_decision)
        evidence_copy = copy.deepcopy(evidence)
        evidence_copy[utility_parents_copy[0]] = 'F'
        evidence_copy[utility_parents_copy[1]] = 'F'
        temporary_output1 = bayes_output_network.prob(evidence_copy)
        temporary_output2 = bayes_output_network.prob(evidence)
        final_output_from_temp = temporary_output1 / temporary_output2
        utility_parent_evidence[utility_parents_not_decision[0]] = 'F'
        utility_parent_evidence[utility_parents_not_decision[1]] = 'F'
        utility_output_4 = final_output_from_temp * \
                           (bayes_output_network.enumerate_ask('utility', utility_parent_evidence))['T']
        return int(round((utility_output_1 + utility_output_2 + utility_output_3 + utility_output_4) + (1e-8)))

    if len(utility_parents_not_decision) == 3:
        utility_parents_copy = copy.deepcopy(utility_parents_not_decision)
        evidence_copy = copy.deepcopy(evidence)
        evidence_copy[utility_parents_copy[0]] = 'T'
        evidence_copy[utility_parents_copy[1]] = 'T'
        evidence_copy[utility_parents_copy[2]] = 'T'
        temporary_output1 = bayes_output_network.prob(evidence_copy)
        temporary_output2 = bayes_output_network.prob(evidence)
        final_output_from_temp = temporary_output1 / temporary_output2
        utility_parent_evidence[utility_parents_not_decision[0]] = 'T'
        utility_parent_evidence[utility_parents_not_decision[1]] = 'T'
        utility_parent_evidence[utility_parents_not_decision[2]] = 'T'
        utility_output_1 = final_output_from_temp * \
                           (bayes_output_network.enumerate_ask('utility', utility_parent_evidence))['T']

        utility_parents_copy = copy.deepcopy(utility_parents_not_decision)
        evidence_copy = copy.deepcopy(evidence)
        evidence_copy[utility_parents_copy[0]] = 'T'
        evidence_copy[utility_parents_copy[1]] = 'T'
        evidence_copy[utility_parents_copy[2]] = 'F'
        temporary_output1 = bayes_output_network.prob(evidence_copy)
        temporary_output2 = bayes_output_network.prob(evidence)
        final_output_from_temp = temporary_output1 / temporary_output2
        utility_parent_evidence[utility_parents_not_decision[0]] = 'T'
        utility_parent_evidence[utility_parents_not_decision[1]] = 'T'
        utility_parent_evidence[utility_parents_not_decision[2]] = 'F'
        utility_output_2 = final_output_from_temp * \
                           (bayes_output_network.enumerate_ask('utility', utility_parent_evidence))['T']

        utility_parents_copy = copy.deepcopy(utility_parents_not_decision)
        evidence_copy = copy.deepcopy(evidence)
        evidence_copy[utility_parents_copy[0]] = 'T'
        evidence_copy[utility_parents_copy[1]] = 'F'
        evidence_copy[utility_parents_copy[2]] = 'T'
        temporary_output1 = bayes_output_network.prob(evidence_copy)
        temporary_output2 = bayes_output_network.prob(evidence)
        final_output_from_temp = temporary_output1 / temporary_output2
        utility_parent_evidence[utility_parents_not_decision[0]] = 'T'
        utility_parent_evidence[utility_parents_not_decision[1]] = 'F'
        utility_parent_evidence[utility_parents_not_decision[2]] = 'T'
        utility_output_3 = final_output_from_temp * \
                           (bayes_output_network.enumerate_ask('utility', utility_parent_evidence))['T']

        utility_parents_copy = copy.deepcopy(utility_parents_not_decision)
        evidence_copy = copy.deepcopy(evidence)
        evidence_copy[utility_parents_copy[0]] = 'T'
        evidence_copy[utility_parents_copy[1]] = 'F'
        evidence_copy[utility_parents_copy[2]] = 'F'
        temporary_output1 = bayes_output_network.prob(evidence_copy)
        temporary_output2 = bayes_output_network.prob(evidence)
        final_output_from_temp = temporary_output1 / temporary_output2
        utility_parent_evidence[utility_parents_not_decision[0]] = 'T'
        utility_parent_evidence[utility_parents_not_decision[1]] = 'F'
        utility_parent_evidence[utility_parents_not_decision[2]] = 'F'
        utility_output_4 = final_output_from_temp * \
                           (bayes_output_network.enumerate_ask('utility', utility_parent_evidence))['T']

        utility_parents_copy = copy.deepcopy(utility_parents_not_decision)
        evidence_copy = copy.deepcopy(evidence)
        evidence_copy[utility_parents_copy[0]] = 'F'
        evidence_copy[utility_parents_copy[1]] = 'T'
        evidence_copy[utility_parents_copy[2]] = 'T'
        temporary_output1 = bayes_output_network.prob(evidence_copy)
        temporary_output2 = bayes_output_network.prob(evidence)
        final_output_from_temp = temporary_output1 / temporary_output2
        utility_parent_evidence[utility_parents_not_decision[0]] = 'F'
        utility_parent_evidence[utility_parents_not_decision[1]] = 'T'
        utility_parent_evidence[utility_parents_not_decision[2]] = 'T'
        utility_output_5 = final_output_from_temp * \
                           (bayes_output_network.enumerate_ask('utility', utility_parent_evidence))['T']

        utility_parents_copy = copy.deepcopy(utility_parents_not_decision)
        evidence_copy = copy.deepcopy(evidence)
        evidence_copy[utility_parents_copy[0]] = 'F'
        evidence_copy[utility_parents_copy[1]] = 'T'
        evidence_copy[utility_parents_copy[2]] = 'F'
        temporary_output1 = bayes_output_network.prob(evidence_copy)
        temporary_output2 = bayes_output_network.prob(evidence)
        final_output_from_temp = temporary_output1 / temporary_output2
        utility_parent_evidence[utility_parents_not_decision[0]] = 'F'
        utility_parent_evidence[utility_parents_not_decision[1]] = 'T'
        utility_parent_evidence[utility_parents_not_decision[2]] = 'F'
        utility_output_6 = final_output_from_temp * \
                           (bayes_output_network.enumerate_ask('utility', utility_parent_evidence))['T']

        utility_parents_copy = copy.deepcopy(utility_parents_not_decision)
        evidence_copy = copy.deepcopy(evidence)
        evidence_copy[utility_parents_copy[0]] = 'F'
        evidence_copy[utility_parents_copy[1]] = 'F'
        evidence_copy[utility_parents_copy[2]] = 'T'
        temporary_output1 = bayes_output_network.prob(evidence_copy)
        temporary_output2 = bayes_output_network.prob(evidence)
        final_output_from_temp = temporary_output1 / temporary_output2
        utility_parent_evidence[utility_parents_not_decision[0]] = 'F'
        utility_parent_evidence[utility_parents_not_decision[1]] = 'F'
        utility_parent_evidence[utility_parents_not_decision[2]] = 'T'
        utility_output_7 = final_output_from_temp * \
                           (bayes_output_network.enumerate_ask('utility', utility_parent_evidence))['T']

        utility_parents_copy = copy.deepcopy(utility_parents_not_decision)
        evidence_copy = copy.deepcopy(evidence)
        evidence_copy[utility_parents_copy[0]] = 'F'
        evidence_copy[utility_parents_copy[1]] = 'F'
        evidence_copy[utility_parents_copy[2]] = 'F'
        temporary_output1 = bayes_output_network.prob(evidence_copy)
        temporary_output2 = bayes_output_network.prob(evidence)
        final_output_from_temp = temporary_output1 / temporary_output2
        utility_parent_evidence[utility_parents_not_decision[0]] = 'F'
        utility_parent_evidence[utility_parents_not_decision[1]] = 'F'
        utility_parent_evidence[utility_parents_not_decision[2]] = 'F'
        utility_output_8 = final_output_from_temp * \
                           (bayes_output_network.enumerate_ask('utility', utility_parent_evidence))['T']

        return int(round((
                             utility_output_1 + utility_output_2 + utility_output_3 + utility_output_4 + utility_output_5 + utility_output_6 + utility_output_7 + utility_output_8) + (
                             1e-8)))
