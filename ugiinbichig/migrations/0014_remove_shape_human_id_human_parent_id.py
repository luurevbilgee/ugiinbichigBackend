# Generated by Django 5.1.3 on 2024-12-11 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugiinbichig', '0013_alter_shape_human_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shape',
            name='human_ID',
        ),
        migrations.AddField(
            model_name='human',
            name='parent_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]