# form校验器
def validate_form(form):
    if not form.validate():
        errors = [u'有错误发生:']
        for k, v in form.errors.items():
            for m in v:
                errors.append(u'%s:%s' % (getattr(form, k).label.text, m))
        raise Exception(u'<br/>'.join(errors))


class Singleton(type):
    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(Singleton, cls).__call__(*args)
        return cls._inst[cls]
