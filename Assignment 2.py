def is_valid_expression(object, function_symbols, leaf_symbols):
    if type(object) is int:
        return True

    if object in leaf_symbols:
        return True

    if type(object) is list and len(object) == 3:
        if (object[0] in function_symbols and 
            is_valid_expression(object[1], function_symbols, leaf_symbols) and
            is_valid_expression(object[2], function_symbols, leaf_symbols)):
            
            return True

    return False



def depth(expression):
    if type(expression) is not list:
        return 0

    else:
        return 1 + max(depth(expression[1]), depth(expression[2]))



def evaluate(expression, bindings):
    if type(expression) is int:
        return expression

    if type(expression) is str:
        return bindings[expression]

    if type(expression) is list and len(expression) == 3:
        return bindings[expression[0]](evaluate(expression[1], bindings), evaluate(expression[2], bindings))



import random
def random_expression(function_symbols, leaves, max_depth):
    res = random.choice('HT')
    if res == 'H' or max_depth == 0:
        return random.choice(leaves)
    
    else:
        return ([random.choice(function_symbols),
                random_expression(function_symbols, leaves, max_depth - 1),
                random_expression(function_symbols, leaves, max_depth - 1)])


def generate_rest(initial_sequence, expression, length):
    i = len(initial_sequence)
    bindings = {'i' : i,
                'x' : initial_sequence[i - 2],
                'y' : initial_sequence[i - 1], 
                '+' : lambda x, y : x + y,
                '-' : lambda x, y : x - y,
                '*' : lambda x, y : x * y}
    
    res = []   
    for _ in range(length):
        lists = initial_sequence + res

        i = len(lists)
        bindings['i'] = i
        bindings['x'] = lists[i - 2]
        bindings['y'] = lists[i - 1]

        res.append(evaluate(expression, bindings))

    return res



def predict_rest(sequence):
    function_symbols = ['+', '-', '*']
    integer = [-2, -1, 0, 1, 2]
    leaves = ['x', 'y', 'i'] + integer
    max_depth = 3

    while True:
        expression = random_expression(function_symbols, leaves, max_depth)
        generate = generate_rest(sequence[:3], expression, len(sequence) - 3)
        if generate == sequence[3:]:
            return generate_rest(sequence, expression, 5)


sequence = [1, 3, -5, 13, -31, 75, -181, 437]
print(predict_rest(sequence))
