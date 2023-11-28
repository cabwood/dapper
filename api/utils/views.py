class ViewMixinMeta(type):
    @property
    def full_name(cls):
        return cls.get_full_name()
    @property
    def full_route(cls):
        return cls.get_full_route()


class ViewMixin(metaclass=ViewMixinMeta):

    name_prefix = None
    name = None

    route_prefix = None
    route = None

    @classmethod
    def get_full_route(cls):
        return f'{cls.route_prefix}{cls.route}' if cls.route_prefix else cls.route

    @classmethod
    def get_full_name(cls):
        return f'{cls.name_prefix}_{cls.name}' if cls.name_prefix else cls.name

    @classmethod
    def get_view_func(cls):
         return cls.as_view(cls.get_full_name())

    @classmethod
    def register_rule(cls, app):
        app.add_url_rule(cls.get_full_route(), view_func=cls.get_view_func())

