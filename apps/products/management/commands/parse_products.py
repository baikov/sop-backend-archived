from django.core.management.base import BaseCommand
from loguru import logger

from apps.products.tasks import parse_products_task


class Command(BaseCommand):
    help = "Парсинг продуктов"

    def handle(self, *args, **options):
        result = parse_products_task.delay()
        result.wait()

        logger.info("Результат: {}", result.successful())
