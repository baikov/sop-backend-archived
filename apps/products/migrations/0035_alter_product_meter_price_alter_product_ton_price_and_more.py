# Generated by Django 4.2.2 on 2023-06-25 13:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0034_product_always_in_stock_product_custom_ton_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="meter_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                help_text="Рассчитывается автоматически, если указан вес метра",
                max_digits=20,
                verbose_name="Цена за метр",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="ton_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                help_text="Спаршеная цена за тонну, обновляется сама",
                max_digits=20,
                verbose_name="Цена за тонну",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="unit_price",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                help_text="Рассчитывается автоматически, если указан вес метра и длина",
                max_digits=20,
                verbose_name="Цена за штуку",
            ),
        ),
        migrations.DeleteModel(
            name="PropertyValue",
        ),
    ]
