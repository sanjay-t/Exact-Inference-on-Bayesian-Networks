import copy


def calculate_probability(queries, bayes_output_network):
    if '|' in queries[1]:
        evidence = dict()
        if len(queries[1]) > 3:
            no_queries_on_lhs = (len(queries[1]) - 1) / 2
            for i in range(2, len(queries)):
                evidence[queries[i][0]] = queries[i][1]
            output_from_lhs = []
            i = 0
            temporary_evidence = copy.deepcopy(evidence)
            while i < no_queries_on_lhs * 2:
                if queries[1][i + 1] == 'T':
                    temporary_evidence[queries[1][i]] = 'T'
                else:
                    temporary_evidence[queries[1][i]] = 'F'
                i += 2
            output_from_lhs.append(float('%0.3f' % round(bayes_output_network.prob(temporary_evidence), 3)))
            output_from_lhs.append(float('%0.3f' % round(bayes_output_network.prob(evidence), 3)))
            return float(('%0.2f' % round((output_from_lhs[0] / output_from_lhs[1]) + (1e-8), 2)))
        else:
            first = queries[1][0]
            for i in range(2, len(queries)):
                evidence[queries[i][0]] = queries[i][1]
            if queries[1][1] == 'T':
                return '%0.2f' % round((bayes_output_network.enumerate_ask(first, evidence)['T']) + (1e-8), 2)
            else:
                return '%0.2f' % round((bayes_output_network.enumerate_ask(first, evidence)['F']) + (1e-8), 2)
    else:
        evidence = dict()
        for i in range(1, len(queries)):
            evidence[queries[i][0]] = queries[i][1]
        return '%0.2f' % round((bayes_output_network.prob(evidence)) + (1e-8), 2)
