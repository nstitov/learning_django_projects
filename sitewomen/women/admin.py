from typing import Any

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.safestring import mark_safe

from .models import Category, Women


# Register your models here.
class MarriedFilter(admin.SimpleListFilter):
    title = "Статус женщин"
    parameter_name = "status"

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ("married", "Замужем"),
            ("single", "Не замужем"),
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == "married":
            return queryset.filter(husband__isnull=False)
        elif self.value() == "single":
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ["title", "slug", "content", "photo", "cat", "husband", "tags"]
    readonly_fields = ["post_photo"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]

    list_display = ["title", "post_photo", "time_create", "is_published"]
    list_display_links = ["title"]
    ordering = ["-time_create", "title"]
    list_editable = ["is_published"]
    actions = ["set_published", "set_draft"]
    search_fields = ["title__startswith"]
    list_filter = [MarriedFilter, "cat__name", "is_published"]

    save_on_top = True

    @admin.display(description="Краткое описание")
    def post_photo(self, women: Women) -> str:
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return "Без фото"

    @admin.action(description="Опубликоовать выбранные записи")
    def set_published(self, request: HttpRequest, queryset: QuerySet) -> None:
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request: HttpRequest, queryset: QuerySet) -> None:
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(
            request, f"{count} записи(ей) сняты с публикации!", messages.WARNING
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
