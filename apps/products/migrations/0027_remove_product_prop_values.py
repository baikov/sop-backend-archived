# Generated by Django 4.2 on 2023-04-25 21:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0026_alter_productpropertyvalue_property_propertyvalue_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="prop_values",
        ),
    ]