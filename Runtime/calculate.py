from Parse.lexing import *
from Parse.treeify import *
from evaluate import *



def print_result(result, ln_name):
    ln_name = ln_name + ': '
    space = ' ' * len(ln_name)
    lines = str(result).split('\n')
    pre = [ln_name] + (len(lines)-1) * [space]
    
    lines = [p+l for p,l in zip(pre, lines)]
    
    print(*lines, sep='\n')



def calc(query, environment, debug=False):
        
#     commands
#     if   query == 'exit':   break
#     elif query == 'help':   help()
#     elif query == 'ref':    ref()
#     elif query == 'clear':  clear()
#     elif query == 'copy':   pyperclip.copy(ans)
#     elif query == '=':      pyperclip.copy(ans)

#     # evaluate query
#     elif query != "":
    

#     if debug: print('environment', environment, end='\n\n')
    
    tokens = lexing(query, environment.ans_available)
    if debug: print('tokens', tokens, end='\n\n')
    
    token_tree = build_token_tree(tokens)
    if debug: print('token_tree', token_tree, end='\n\n')
    
    computation_graph = build_computation_graph(token_tree)
    if debug: print('computation_graph', computation_graph, end='\n\n')
    
    result = evaluate(computation_graph, environment)
    
    ln_name = environment.addLn(result)
    print_result(result, ln_name)

    return result