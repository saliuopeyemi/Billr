


def ensure_value_is_a_list(value,fail_function,*args,**kwargs):
    if not isinstance(value,list):
        fail_function(*args,**kwargs)
    return True


def retrieve_query_parameter(request,parameter,fail_function,*args,**kwargs):
    param = request.query_params.get(parameter)
    if not param:
        fail_function(*args,**kwargs)
    else:
        return param


def retrieve_object(obj_id,db_model,fail_function,*args,**kwargs):
    obj = db_model.objects.filter(id=obj_id).first()
    if not obj:
        fail_function(*args,**kwargs)
    else:
        return obj

