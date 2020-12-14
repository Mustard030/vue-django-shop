# Generated by Django 3.1.2 on 2020-12-14 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20201214_1459'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodskind',
            old_name='kind_name',
            new_name='mainKind',
        ),
        migrations.AddField(
            model_name='goodskind',
            name='secondKind',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.goodskind'),
        ),
    ]