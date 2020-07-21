from Classes.built_ins import built_ins
from Classes.data_structures import *
from Classes.data_types import *



def group_round(environment, items, shape, force_array=False, **kwargs):
    
    if shape == () and force_array == False:
        return items[0]
    else:
        return Array(items)

built_ins.register_grouping('(', ')', {',': 1, '\n': 1}, True, group_round)



def group_squre(environment, items, shape, **kwargs):
    
    assert len(items) > 0, 'Tensors can not be empty'
    
    base_shape = items[0].shape
    assert all([i.shape == base_shape for i in items]), 'Tensor elements have inconsistent shapes'
    
    extended_shape = shape + base_shape
    data = np.array([i.data for i in items]).reshape(extended_shape)
    
    return Tensor(data, extended_shape)

built_ins.register_grouping('[', ']', {',': 1, ';': 2, '\n': 0}, False, group_squre)



def group_curly(environment, items, shape, **kwargs):
    return items[-1]

built_ins.register_grouping('{', '}', {';': 1, '\n': 1}, True, group_curly)



def group_straight(environment, items, shape, **kwargs):
    
    assert shape == (), 'Cannot take absolute value of an array'
    assert items[0].dtype == Real, 'Cannot take absolute value of non Real value'
    
#     return Tensor(Real(abs(items[0].first.value)))

    return VariableFunction('abs', items).eval(environment)

built_ins.register_grouping('|', '|', {}, True, group_straight)
built_ins.register_grouping('||', '||', {}, True, group_straight)