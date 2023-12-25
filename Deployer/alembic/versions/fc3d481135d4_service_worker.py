"""service-worker

Revision ID: fc3d481135d4
Revises: bea454ec661d
Create Date: 2023-12-22 03:52:14.688471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc3d481135d4'
down_revision: Union[str, None] = 'bea454ec661d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    service_worker_status_table = op.create_table(
        "service_worker_status",
        sa.Column("completed_transaction_count", sa.Integer, nullable=False),
        sa.Column("is_done", sa.Boolean, default=False)
    )
    op.bulk_insert(service_worker_status_table, [{"completed_transaction_count": 0}])
    op.create_table(
        'location_info',
        sa.Column('location_info_id', sa.BigInteger, primary_key=True),
        sa.Column('region_name', sa.String(255), nullable=False),
        sa.Column('area_name', sa.String(255), nullable=False),
        sa.Column('territory_name', sa.String(255), nullable=False),
    )
    op.create_table(
        'person_location_info',
        sa.Column('person_location_info_id', sa.BigInteger, primary_key=True),
        sa.Column('person_location_type', sa.String(256), nullable=False),
        sa.Column('location_info_id', sa.BigInteger, nullable=False),
        sa.ForeignKeyConstraint(('location_info_id',), ['location_info.location_info_id'], )
    )
    op.create_table(
        'learning_profile',
        sa.Column('learning_profile_id', sa.BigInteger, primary_key=True),
        sa.Column('learning_profile_name', sa.String(256), nullable=False),
        sa.Column('learning_profile_language', sa.String(256), nullable=False),
    )
    op.create_table(
        'educational_institution',
        sa.Column('educational_institution_id', sa.BigInteger, primary_key=True),
        sa.Column('educational_institution_name', sa.String(256), nullable=False),
        sa.Column('educational_institution_parent', sa.String(256), nullable=False),
        sa.Column('educational_institution_type', sa.String(256), nullable=False),
        sa.Column('location_info_id', sa.BigInteger, nullable=False),
        sa.ForeignKeyConstraint(('location_info_id',), ['location_info.location_info_id'], )
    )
    op.create_table(
        'person',
        sa.Column('person_id', sa.BigInteger, primary_key=True),
        sa.Column('person_out_id', sa.String(256), nullable=False),
        sa.Column('birth', sa.SmallInteger, nullable=False),
        sa.Column('registration_status', sa.String(256), nullable=False),
        sa.Column('sex_type', sa.String(256), nullable=False),
        sa.Column('learning_profile_id', sa.BigInteger, nullable=True),
        sa.Column('educational_institution_id', sa.BigInteger, nullable=True),
        sa.Column('person_location_info_id', sa.BigInteger, nullable=False),
        sa.ForeignKeyConstraint(('learning_profile_id',), ['learning_profile.learning_profile_id'], ),
        sa.ForeignKeyConstraint(('educational_institution_id',), ['educational_institution.educational_institution_id'], ),
        sa.ForeignKeyConstraint(('person_location_info_id',), ['person_location_info.person_location_info_id'], )
    )
    op.create_table(
        'test_institution',
        sa.Column('test_institution_id', sa.BigInteger, primary_key=True),
        sa.Column('test_institution_name', sa.String(256), nullable=False),
        sa.Column('location_info_id', sa.BigInteger, nullable=False),
        sa.ForeignKeyConstraint(('location_info_id',), ['location_info.location_info_id'], )
    )
    op.create_table(
        'test_result',
        sa.Column('test_result_id', sa.BigInteger, primary_key=True),
        sa.Column('subject_name', sa.String(28), nullable=False),
        sa.Column('test_status', sa.String(256), nullable=False),
        sa.Column('test_language', sa.String(256), nullable=True),
        sa.Column('dpa_level', sa.String(256), nullable=True),
        sa.Column('ball_100', sa.DECIMAL, nullable=True),
        sa.Column('ball_12', sa.SmallInteger, nullable=True),
        sa.Column('ball', sa.SmallInteger, nullable=True),
        sa.Column('adapt_scale', sa.SmallInteger, nullable=True),
        sa.Column('year_of_attempt', sa.SmallInteger, nullable=False),
    )
    op.create_table(
        'p_ti_tr',
        sa.Column('person_id', sa.BigInteger, nullable=False),
        sa.Column('test_institution_id', sa.BigInteger, nullable=False),
        sa.Column('test_result_id', sa.BigInteger, nullable=False),
        sa.ForeignKeyConstraint(('person_id',), ['person.person_id'], ),
        sa.ForeignKeyConstraint(('test_institution_id',), ['test_institution.test_institution_id'], ),
        sa.ForeignKeyConstraint(('test_result_id',), ['test_result.test_result_id'], )
    )


def downgrade() -> None:
    op.drop_table('service_worker_status')
    op.drop_table('p_ti_tr')
    op.drop_table('test_result')
    op.drop_table('test_institution')
    op.drop_table('person')
    op.drop_table('educational_institution')
    op.drop_table('learning_profile')
    op.drop_table('person_location_info')
    op.drop_table('location_info')
