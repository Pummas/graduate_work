# Generated by Django 3.2 on 2023-04-15 20:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import movies.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filmwork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('creation_date', models.DateField(verbose_name='creation date')),
                ('file', models.FileField(upload_to=movies.models.set_filename, verbose_name='file')),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='rating')),
                ('type', models.CharField(choices=[('movie', 'movie'), ('tv_show', 'tv_show')], help_text='Выберите тип произведения', max_length=7, verbose_name='type')),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('failed', 'Failed'), ('done', 'Done')], default='waiting', max_length=50, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Кинопроизведение',
                'verbose_name_plural': 'Кинопроизведения',
                'db_table': 'content"."film_work',
                'ordering': ('-creation_date',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'db_table': 'content"."genre',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255, verbose_name='full name')),
            ],
            options={
                'verbose_name': 'Участник',
                'verbose_name_plural': 'Участники',
                'db_table': 'content"."person',
                'ordering': ('full_name',),
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('size', models.PositiveBigIntegerField(help_text='Enter the storage size in gigabytes', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(15360)], verbose_name='size')),
                ('url', models.CharField(max_length=200, verbose_name='url')),
                ('geo_ip', models.GenericIPAddressField(verbose_name='geo_ip')),
            ],
            options={
                'verbose_name': 'Хранилище',
                'verbose_name_plural': 'Хранилища',
                'db_table': 'content"."storage',
                'ordering': ('-size',),
            },
        ),
        migrations.CreateModel(
            name='PersonFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.TextField(choices=[('actor', 'actor'), ('director', 'director'), ('writer', 'writer')], max_length=8, null=True, verbose_name='role')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.person')),
            ],
            options={
                'verbose_name': 'Участник фильма',
                'verbose_name_plural': 'Участники фильма',
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.CreateModel(
            name='GenreFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.genre')),
            ],
            options={
                'verbose_name': 'Жанр фильма',
                'verbose_name_plural': 'Жанры фильма',
                'db_table': 'content"."genre_film_work',
            },
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.GenreFilmwork', to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilmwork', to='movies.Person'),
        ),
        migrations.AddConstraint(
            model_name='personfilmwork',
            constraint=models.UniqueConstraint(fields=('film_work', 'person', 'role'), name='unique_film_work_person'),
        ),
        migrations.AddConstraint(
            model_name='genrefilmwork',
            constraint=models.UniqueConstraint(fields=('film_work', 'genre'), name='unique_film_work_genre'),
        ),
    ]
