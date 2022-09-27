# Generated by Django 3.2 on 2022-09-27 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='categories/images/'),
        ),
        migrations.CreateModel(
            name='SpecificationOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specification_option', to='base.specification')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.specificationoption')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.product')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.specification')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_specifications',
            field=models.ManyToManyField(related_name='specifications', through='base.ProductSpecification', to='base.SpecificationOption'),
        ),
    ]
