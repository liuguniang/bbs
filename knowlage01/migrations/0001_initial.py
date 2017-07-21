# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 11:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='article',
            fields=[
                ('aid', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='文章题目')),
                ('summary', models.TextField(verbose_name='文章摘要')),
                ('create_time', models.DateTimeField(verbose_name='发布时间')),
                ('read_count', models.IntegerField(verbose_name='阅读数')),
                ('comment_count', models.IntegerField(verbose_name='评论数')),
                ('up_count', models.IntegerField(null=True, verbose_name='点赞数')),
                ('dowm_count', models.IntegerField(null=True, verbose_name='点踩数')),
                ('type', models.IntegerField(choices=[(1, 'Python'), (2, 'Linux'), (3, 'Go'), (4, 'Java')], verbose_name='类型')),
            ],
        ),
        migrations.CreateModel(
            name='article_tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='knowlage01.article')),
            ],
        ),
        migrations.CreateModel(
            name='blog',
            fields=[
                ('bid', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='博客标题')),
                ('theme', models.IntegerField(verbose_name='博客主题')),
                ('site', models.CharField(max_length=64, verbose_name='博客后缀')),
            ],
        ),
        migrations.CreateModel(
            name='classfiy',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('classfiy', models.CharField(max_length=64, verbose_name='分类')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowlage01.blog')),
            ],
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(verbose_name='评论时间')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowlage01.article', verbose_name='评论的文章')),
                ('parent_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='knowlage01.comment')),
            ],
        ),
        migrations.CreateModel(
            name='content',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(verbose_name='文章内容')),
            ],
        ),
        migrations.CreateModel(
            name='fans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='tag',
            fields=[
                ('tid', models.BigAutoField(primary_key=True, serialize=False)),
                ('tag', models.CharField(max_length=64, verbose_name='标签')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowlage01.blog')),
            ],
        ),
        migrations.CreateModel(
            name='updown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.BooleanField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowlage01.article', verbose_name='点赞的文章')),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('uid', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=64, unique=True, verbose_name='用户名')),
                ('password', models.IntegerField(unique=True, verbose_name='密码')),
                ('nickname', models.CharField(max_length=64, unique=True, verbose_name='昵称')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='邮箱')),
                ('avator', models.ImageField(upload_to='', verbose_name='头像')),
                ('create_time', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='updown',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowlage01.user', verbose_name='点赞/踩的用户'),
        ),
        migrations.AddField(
            model_name='fans',
            name='fan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fan', to='knowlage01.user'),
        ),
        migrations.AddField(
            model_name='fans',
            name='faned',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faned', to='knowlage01.user'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowlage01.user', verbose_name='评论的用户'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='knowlage01.user'),
        ),
        migrations.AddField(
            model_name='article_tag',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='knowlage01.tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowlage01.blog', verbose_name='所属博客'),
        ),
        migrations.AddField(
            model_name='article',
            name='classfiy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='knowlage01.classfiy', verbose_name='分类'),
        ),
        migrations.AddField(
            model_name='article',
            name='content',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='knowlage01.content'),
        ),
        migrations.AlterUniqueTogether(
            name='updown',
            unique_together=set([('user', 'article')]),
        ),
        migrations.AlterUniqueTogether(
            name='fans',
            unique_together=set([('faned', 'fan')]),
        ),
        migrations.AlterUniqueTogether(
            name='article_tag',
            unique_together=set([('article', 'tag')]),
        ),
    ]
