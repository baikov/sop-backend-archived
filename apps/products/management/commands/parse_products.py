from django.core.management.base import BaseCommand
from loguru import logger

from apps.products.tasks import parse_products_task


class Command(BaseCommand):
    help = "Парсинг продуктов"

    def add_arguments(self, parser):
        parser.add_argument(
            "--cat_ids",
            dest="cat_ids",
            type=str,
            help="ID категорий для парсинга, разделенные запятыми",
        )

    def handle(self, *args, **options):
        cat_ids = options.get("cat_ids", [])
        if cat_ids:
            cat_ids_list = cat_ids.split(",")
        result = parse_products_task.delay(cat_ids_list)
        result.wait()

        logger.info("Результат: {}", result.successful())
