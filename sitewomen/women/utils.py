from typing import Any

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


class DataMixin:
    title_page = None
    paginate_by = 2
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context["title"] = self.title_page

        if "menu" not in self.extra_context:
            self.extra_context["menu"] = menu

    def get_mixin_context(self, context: dict[str, Any], **kwargs: dict[str, Any]):
        if self.title_page:
            context["title"] = self.title_page

        context["menu"] = menu
        context["cat_selected"] = None
        context.update(kwargs)
        return context
