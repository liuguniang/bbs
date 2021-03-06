# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 12:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knowlage01', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='content',
        ),
        migrations.AddField(
            model_name='content',
            name='article',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='knowlage01.article', verbose_name='所属文章'),
        ),
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='发布时间'),
        ),
        migrations.AlterField(
            model_name='article',
            name='summary',
            field=models.CharField(max_length=225, verbose_name='文章摘要'),
        ),
        migrations.AlterField(
            model_name='article',
            name='type',
            field=models.IntegerField(choices=[(1, 'Python'), (2, 'Linux'), (3, 'Go'), (4, 'Java')], default=None, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='site',
            field=models.CharField(max_length=64, unique=True, verbose_name='博客后缀'),
        ),
        migrations.AlterField(
            model_name='classfiy',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowlage01.blog', verbose_name='所属博客'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=225, verbose_name='评论内容'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='knowlage01.comment', verbose_name='回复评论'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowlage01.blog', verbose_name='所属博客'),
        ),
        migrations.AlterField(
            model_name='updown',
            name='type',
            field=models.BooleanField(verbose_name='是否赞'),
        ),
    ]
