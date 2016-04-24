def extend(d, k, v):
    n = d.copy()
    n[k] = v
    return n


def cut(d, k):
    if isinstance(d, dict):
        n = d.copy()
        if k in n:
            del n[k]
        return n
    return [v for v in d if v != k]


def normalize(dist):
    if isinstance(dist, dict):
        keys = dist.keys()
        values = [dist[k] for k in keys]
        normalize(values)
        for k, v in zip(keys, values):
            dist[k] = v
        return
    fdist = [float(d) for d in dist]
    s = sum(fdist)
    if s == 0:
        return
    fdist = [d / s for d in fdist]
    for i, d in enumerate(fdist):
        dist[i] = d


class DiscreteCPT(object):
    def __init__(self, values, probability_table):
        self.my_values = values
        if isinstance(probability_table, list) or isinstance(probability_table, tuple):
            self.probability_table = {(): probability_table}
        else:
            self.probability_table = probability_table

    def values(self):
        return self.my_values

    def prob_dist(self, parent_values):
        if isinstance(parent_values, list):
            parent_values = tuple(parent_values)
        return dict([(self.my_values[i], p) for i, p in enumerate(self.probability_table[parent_values])])


class DiscreteBayesNode(object):
    def __init__(self, name, parents, cpt):
        self.parents = parents
        self.name = name
        self.cpt = cpt


class DiscreteBayesNet(object):
    def __init__(self, nodes):
        self.variables = dict([(n.name, n) for n in nodes])
        self.roots = [n for n in nodes if not n.parents]
        self.nodes = nodes

    def enumerate_ask(self, var, e):
        values = self.variables[var].cpt.values()
        dist = {}
        if var in e:
            for v in values:
                dist[v] = 1.0 if e[var] == v else 0.0
            return dist

        for v in values:
            dist[v] = self.enumerate_all(self.variables,
                                         extend(e, var, v))
        normalize(dist)
        return dist

    def enumerate_all(self, variables, e, v=None):
        if len(variables) == 0:
            return 1.0
        if v:
            Y = v
        else:
            Y = variables.keys()[0]
        Ynode = self.variables[Y]
        parents = Ynode.parents
        cpt = Ynode.cpt
        # Work up the graph if necessary
        for p in parents:
            if p not in e:
                return self.enumerate_all(variables, e, p)
        if Y in e:
            y = e[Y]
            # P(y | parents(Y))
            cp = cpt.prob_dist([e[p] for p in parents])[y]
            result = cp * self.enumerate_all(cut(variables, Y), e)
        else:
            result = 0
            for y in Ynode.cpt.values():
                # P(y | parents(Y))
                cp = cpt.prob_dist([e[p] for p in parents])[y]
                result += cp * self.enumerate_all(cut(variables, Y),
                                                  extend(e, Y, y))
        return result

    def prob(self, e):
        return self.enumerate_all(self.variables, e)
