# Generated by Django 2.0.4 on 2020-05-05 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0007_invoice_invoicedetail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoicedetail',
            old_name='Food',
            new_name='food',
        ),
    ]