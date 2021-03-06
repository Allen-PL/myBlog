# Generated by Django 2.0.5 on 2020-03-28 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200328_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='article_id',
            field=models.ForeignKey(on_delete=None, to='blog.Article', verbose_name='关联文章'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_id',
            field=models.OneToOneField(default=0, null=True, on_delete=None, to='blog.Comment', verbose_name='自关联'),
        ),
    ]
