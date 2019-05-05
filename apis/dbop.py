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