from django.core.management.base import BaseCommand

from apps.products.models import Category
from apps.products.tasks import parse_category_products_task
from apps.utils.custom import get_object_or_None


class Command(BaseCommand):
    help = "Парсинг продуктов"

    def handle(self, *args, **options):
        category = get_object_or_None(Category, name="Трубы ВГП")
        if category:
            result = parse_category_products_task.delay(category_id=category.id)
            result.wait()
            self.stdout.write(self.style.SUCCESS(f"Результат: {result.successful()}"))
        else:
            self.stdout.write(self.style.ERROR("Категория не найдена в БД"))
