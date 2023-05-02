from django.core.management.base import BaseCommand
from django.db import connection

from apps.products.models import Category
from apps.products.tasks import parse_categories_task


class Command(BaseCommand):
    help = "Парсинг категорий с сайта mc.ru и сохранение в БД"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clean", dest="clean", type=bool, help="Clean DB", default=True
        )
        parser.add_argument(
            "--reset-seq", dest="reset-seq", type=bool, help="Reset seq", default=True
        )

    def handle(self, *args, **options):
        if options.get("clean"):
            # Очищаем таблицу Category
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Очищена таблица categories"))
        if options.get("reset-seq"):
            # Обнуляем нумерацию индексов
            with connection.cursor() as cursor:
                cursor.execute("ALTER SEQUENCE products_category_id_seq RESTART WITH 1")

            # with connection.cursor() as cursor:
            #     cursor.execute(
            #         """
            #         SELECT setval(pg_get_serial_sequence('"products_category"','id'),
            #         coalesce(max("id"), 1),
            #         max("id") IS NOT null) FROM "products_category";
            #     """
            #     )
            self.stdout.write(
                self.style.SUCCESS(
                    "Сброшена нумерация индексов таблицы products_category"
                )
            )
        parse_categories_task.delay()
        # result = categories_parser.delay()
        # logger.debug("result.id: {}", result.id)
