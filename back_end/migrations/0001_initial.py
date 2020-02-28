# Generated by Django 3.0.2 on 2020-02-28 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllocatedEICDetail',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('EntityCreatedAt', models.DateTimeField()),
                ('EntityModifiedAt', models.DateTimeField()),
                ('MRID', models.CharField(blank=True, max_length=250, null=True)),
                ('DocStatusValue', models.CharField(blank=True, max_length=250, null=True)),
                ('AttributeInstanceComponent', models.CharField(blank=True, max_length=250, null=True)),
                ('LongNames', models.CharField(blank=True, max_length=250, null=True)),
                ('DisplayNames', models.CharField(blank=True, max_length=250, null=True)),
                ('LastRequestDateAndOrTime', models.DateTimeField(blank=True, null=True)),
                ('DeactivateRequestDateAndOrTime', models.DateTimeField(blank=True, null=True)),
                ('MarketParticipantStreetAddressCountry', models.CharField(blank=True, max_length=250, null=True)),
                ('MarketParticipantACERCode', models.CharField(blank=True, max_length=250, null=True)),
                ('MarketParticipantVATcode', models.CharField(blank=True, max_length=250, null=True)),
                ('Description', models.CharField(blank=True, max_length=255, null=True)),
                ('EICParentMarketDocumentMRID', models.CharField(blank=True, max_length=250, null=True)),
                ('ELCResponsibleMarketParticipantMRID', models.CharField(blank=True, max_length=250, null=True)),
                ('IsDeleted', models.BooleanField()),
                ('AllocatedEICID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AreaTypeCode',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('EntityCreatedAt', models.DateTimeField()),
                ('EntityModifiedAt', models.DateTimeField()),
                ('AreaTypeCodeText', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('AreaTypeCodeNote', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MapCode',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('EntityCreatedAt', models.DateTimeField()),
                ('EntityModifiedAt', models.DateTimeField()),
                ('MapCodeText', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('MapCodeNote', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductionType',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('EntityCreatedAt', models.DateTimeField()),
                ('EntityModifiedAt', models.DateTimeField()),
                ('ProductionTypeText', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('ProductionTypeNote', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResolutionCode',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('EntityCreatedAt', models.DateTimeField()),
                ('EntityModifiedAt', models.DateTimeField()),
                ('ResolutionCodeText', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('ResolutionCodeNote', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DayAheadTotalLoadForecast',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('EntityCreatedAt', models.DateTimeField()),
                ('EntityModifiedAt', models.DateTimeField()),
                ('ActionTaskID', models.BigIntegerField()),
                ('Status', models.CharField(blank=True, max_length=2, null=True)),
                ('Year', models.IntegerField()),
                ('Month', models.IntegerField()),
                ('Day', models.IntegerField()),
                ('DateTime', models.DateTimeField()),
                ('AreaName', models.CharField(blank=True, max_length=200, null=True)),
                ('UpdateTime', models.DateTimeField()),
                ('TotalLoadValue', models.DecimalField(decimal_places=2, max_digits=24)),
                ('RowHash', models.CharField(blank=True, max_length=255, null=True)),
                ('AreaCodeId', models.ForeignKey(db_column='AreaCodeId', on_delete=django.db.models.deletion.DO_NOTHING, to='back_end.AllocatedEICDetail')),
                ('AreaTypeCodeId', models.ForeignKey(blank=True, db_column='AreaTypeCodeId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='back_end.AreaTypeCode')),
                ('MapCodeId', models.ForeignKey(blank=True, db_column='MapCodeId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='back_end.MapCode')),
                ('ResolutionCodeId', models.ForeignKey(blank=True, db_column='ResolutionCodeId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='back_end.ResolutionCode')),
            ],
        ),
        migrations.CreateModel(
            name='AggregatedGenerationPerType',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('EntityCreatedAt', models.DateTimeField()),
                ('EntityModifiedAt', models.DateTimeField()),
                ('ActionTaskID', models.BigIntegerField()),
                ('Status', models.CharField(blank=True, max_length=2, null=True)),
                ('Year', models.IntegerField()),
                ('Month', models.IntegerField()),
                ('Day', models.IntegerField()),
                ('DateTime', models.DateTimeField()),
                ('AreaName', models.CharField(blank=True, max_length=200, null=True)),
                ('UpdateTime', models.DateTimeField()),
                ('ActualGenerationOutput', models.DecimalField(decimal_places=2, max_digits=24)),
                ('ActualConsuption', models.DecimalField(decimal_places=2, max_digits=24)),
                ('RowHash', models.CharField(blank=True, max_length=255, null=True)),
                ('AreaCodeId', models.ForeignKey(db_column='AreaCodeId', on_delete=django.db.models.deletion.DO_NOTHING, to='back_end.AllocatedEICDetail')),
                ('AreaTypeCodeId', models.ForeignKey(blank=True, db_column='AreaTypeCodeId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='back_end.AreaTypeCode')),
                ('MapCodeId', models.ForeignKey(blank=True, db_column='MapCodeId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='back_end.MapCode')),
                ('ProductionTypeId', models.ForeignKey(blank=True, db_column='ProductionTypeId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='back_end.ProductionType')),
                ('ResolutionCodeId', models.ForeignKey(blank=True, db_column='ResolutionCodeId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='back_end.ResolutionCode')),
            ],
        ),
        migrations.CreateModel(
            name='ActualTotalLoad',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('EntityCreatedAt', models.DateTimeField()),
                ('EntityModifiedAt', models.DateTimeField()),
                ('ActionTaskID', models.BigIntegerField()),
                ('Status', models.CharField(blank=True, max_length=2, null=True)),
                ('Year', models.IntegerField()),
                ('Month', models.IntegerField()),
                ('Day', models.IntegerField()),
                ('DateTime', models.DateTimeField()),
                ('AreaName', models.CharField(blank=True, max_length=200, null=True)),
                ('UpdateTime', models.DateTimeField()),
                ('TotalLoadValue', models.DecimalField(decimal_places=2, max_digits=24)),
                ('RowHash', models.CharField(blank=True, max_length=255, null=True)),
                ('AreaCodeId', models.ForeignKey(db_column='AreaCodeId', on_delete=django.db.models.deletion.DO_NOTHING, to='back_end.AllocatedEICDetail')),
                ('AreaTypeCodeId', models.ForeignKey(blank=True, db_column='AreaTypeCodeId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='back_end.AreaTypeCode')),
                ('MapCodeId', models.ForeignKey(blank=True, db_column='MapCodeId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='back_end.MapCode')),
                ('ResolutionCodeId', models.ForeignKey(blank=True, db_column='ResolutionCodeId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='back_end.ResolutionCode')),
            ],
        ),
    ]
