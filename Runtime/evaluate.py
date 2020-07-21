def build_computation_graph(token_tree):
    return token_tree.get_evaluable()



def evaluate(computation_graph, environment):
    return computation_graph.eval(environment)