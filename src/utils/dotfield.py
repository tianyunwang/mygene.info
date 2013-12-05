import json


def make_object(attr, value):
    '''
    make_object('a.b.c', 100) -->
    or make_object(['a','b','c'], 100) -->
      {a:{b:{c:100}}}
    '''
    attr_list = attr.split('.')
    s = ''
    for k in attr_list:
    	s += '{"' + k + '":'
    s += json.dumps(value)
    s += "}"* (len(attr_list))
    return json.loads(s)


def merge_object(obj1, obj2):
    for k in obj2:
        try:
            if isinstance(obj2[k], dict):
                obj1[k] = merge_object(obj1[k], obj2[k])
            else:
                obj1[k] = obj2[k]
        except:
            obj1[k] = obj2[k]
    return obj1


def parse_dot_fields(genedoc):
    """
    parse_dot_fields({'a': 1, 'b.c': 2, 'b.a.c': 3})
     should return
        {'a': 1, 'b': {'a': {'c': 3}, 'c': 2}}
    """
    dot_fields = []
    expanded_doc = {}
    for key in genedoc:
        if key.find('.') != -1:
            dot_fields.append(key)
            expanded_doc = merge_object(expanded_doc, make_object(key, genedoc[key]))
    genedoc.update(expanded_doc)
    for key in dot_fields:
        del genedoc[key]
    return genedoc