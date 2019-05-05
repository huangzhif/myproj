class DataOperate(object):
    def __init__(self):
        pass

    @staticmethod
    def delete(model, **kwargs):
        try:
            model.objects.filter(**kwargs).delete()
            status = True
            msg = ""
        except Exception as e:
            status = False
            msg = str(e)
        return status, msg

    @staticmethod
    def get_object(model, **kwargs):
        """
        use this function for query
        使用改封装函数查询数据库
        """
        for value in kwargs.values():
            if not value:
                return None

        the_object = model.objects.filter(**kwargs)
        if len(the_object) == 1:
            the_object = the_object[0]
        else:
            the_object = None
        return the_object
