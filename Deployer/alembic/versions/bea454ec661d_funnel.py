"""funnel

Revision ID: bea454ec661d
Revises: 5092ad38750d
Create Date: 2023-12-22 01:27:38.725070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bea454ec661d'
down_revision: Union[str, None] = '5092ad38750d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    funnel_status_table = op.create_table(
        "funnel_status",
        sa.Column("completed_transaction_count", sa.Integer, nullable=False),
        sa.Column("is_done", sa.Boolean, default=False)
    )
    op.bulk_insert(funnel_status_table, [{"completed_transaction_count": 0}])
    op.create_table(
        "zno",
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('out_id', sa.String(255), nullable=True),
        sa.Column('birth', sa.SmallInteger, nullable=True),
        sa.Column('sextypename', sa.String(255), nullable=True),
        sa.Column('regname', sa.String(255), nullable=True),
        sa.Column('areaname', sa.String(255), nullable=True),
        sa.Column('tername', sa.String(255), nullable=True),
        sa.Column('regtypename', sa.String(255), nullable=True),
        sa.Column('tertypename', sa.String(255), nullable=True),
        sa.Column('classprofilename', sa.String(255), nullable=True),
        sa.Column('classlangname', sa.String(255), nullable=True),
        sa.Column('eoname', sa.String(255), nullable=True),
        sa.Column('eotypename', sa.String(255), nullable=True),
        sa.Column('eoregname', sa.String(255), nullable=True),
        sa.Column('eoareaname', sa.String(255), nullable=True),
        sa.Column('eotertypename', sa.String(255), nullable=True),
        sa.Column('eoparent', sa.String(255), nullable=True),
        sa.Column('ukr_test', sa.String(255), nullable=True),
        sa.Column('ukr_test_status', sa.String(255), nullable=True),
        sa.Column('ukr_ball100', sa.DECIMAL, nullable=True),
        sa.Column('ukr_ball12', sa.SmallInteger, nullable=True),
        sa.Column('ukr_ball', sa.SmallInteger, nullable=True),
        sa.Column('ukr_adapt_scale', sa.SmallInteger, nullable=True),
        sa.Column('ukr_pt_name', sa.String(255), nullable=True),
        sa.Column('ukr_pt_reg_name', sa.String(255), nullable=True),
        sa.Column('ukr_pt_area_name', sa.String(255), nullable=True),
        sa.Column('ukr_pt_ter_name', sa.String(255), nullable=True),
        sa.Column('hist_test', sa.String(255), nullable=True),
        sa.Column('hist_lang', sa.String(255), nullable=True),
        sa.Column('hist_test_status', sa.String(255), nullable=True),
        sa.Column('hist_ball100', sa.DECIMAL, nullable=True),
        sa.Column('hist_ball12', sa.SmallInteger, nullable=True),
        sa.Column('hist_ball', sa.SmallInteger, nullable=True),
        sa.Column('hist_pt_name', sa.String(255), nullable=True),
        sa.Column('hist_pt_reg_name', sa.String(255), nullable=True),
        sa.Column('hist_pt_area_name', sa.String(255), nullable=True),
        sa.Column('hist_pt_ter_name', sa.String(255), nullable=True),
        sa.Column('math_test', sa.String(255), nullable=True),
        sa.Column('math_lang', sa.String(255), nullable=True),
        sa.Column('math_test_status', sa.String(255), nullable=True),
        sa.Column('math_ball100', sa.DECIMAL, nullable=True),
        sa.Column('math_ball12', sa.SmallInteger, nullable=True),
        sa.Column('math_ball', sa.SmallInteger, nullable=True),
        sa.Column('math_pt_name', sa.String(255), nullable=True),
        sa.Column('math_pt_reg_name', sa.String(255), nullable=True),
        sa.Column('math_pt_area_name', sa.String(255), nullable=True),
        sa.Column('math_pt_ter_name', sa.String(255), nullable=True),
        sa.Column('phys_test', sa.String(255), nullable=True),
        sa.Column('phys_lang', sa.String(255), nullable=True),
        sa.Column('phys_test_status', sa.String(255), nullable=True),
        sa.Column('phys_ball100', sa.DECIMAL, nullable=True),
        sa.Column('phys_ball12', sa.SmallInteger, nullable=True),
        sa.Column('phys_ball', sa.SmallInteger, nullable=True),
        sa.Column('phys_pt_name', sa.String(255), nullable=True),
        sa.Column('phys_pt_reg_name', sa.String(255), nullable=True),
        sa.Column('phys_pt_area_name', sa.String(255), nullable=True),
        sa.Column('phys_pt_ter_name', sa.String(255), nullable=True),
        sa.Column('chem_test', sa.String(255), nullable=True),
        sa.Column('chem_lang', sa.String(255), nullable=True),
        sa.Column('chem_test_status', sa.String(255), nullable=True),
        sa.Column('chem_ball100', sa.DECIMAL, nullable=True),
        sa.Column('chem_ball12', sa.SmallInteger, nullable=True),
        sa.Column('chem_ball', sa.SmallInteger, nullable=True),
        sa.Column('chem_pt_name', sa.String(255), nullable=True),
        sa.Column('chem_pt_reg_name', sa.String(255), nullable=True),
        sa.Column('chem_pt_area_name', sa.String(255), nullable=True),
        sa.Column('chem_pt_ter_name', sa.String(255), nullable=True),
        sa.Column('bio_test', sa.String(255), nullable=True),
        sa.Column('bio_lang', sa.String(255), nullable=True),
        sa.Column('bio_test_status', sa.String(255), nullable=True),
        sa.Column('bio_ball100', sa.DECIMAL, nullable=True),
        sa.Column('bio_ball12', sa.SmallInteger, nullable=True),
        sa.Column('bio_ball', sa.SmallInteger, nullable=True),
        sa.Column('bio_pt_name', sa.String(255), nullable=True),
        sa.Column('bio_pt_reg_name', sa.String(255), nullable=True),
        sa.Column('bio_pt_area_name', sa.String(255), nullable=True),
        sa.Column('bio_pt_ter_name', sa.String(255), nullable=True),
        sa.Column('geo_test', sa.String(255), nullable=True),
        sa.Column('geo_lang', sa.String(255), nullable=True),
        sa.Column('geo_test_status', sa.String(255), nullable=True),
        sa.Column('geo_ball100', sa.DECIMAL, nullable=True),
        sa.Column('geo_ball12', sa.SmallInteger, nullable=True),
        sa.Column('geo_ball', sa.SmallInteger, nullable=True),
        sa.Column('geo_pt_name', sa.String(255), nullable=True),
        sa.Column('geo_pt_reg_name', sa.String(255), nullable=True),
        sa.Column('geo_pt_area_name', sa.String(255), nullable=True),
        sa.Column('geo_pt_ter_name', sa.String(255), nullable=True),
        sa.Column('eng_test', sa.String(255), nullable=True),
        sa.Column('eng_test_status', sa.String(255), nullable=True),
        sa.Column('eng_ball100', sa.DECIMAL, nullable=True),
        sa.Column('eng_ball12', sa.SmallInteger, nullable=True),
        sa.Column('eng_dpa_level', sa.String(255), nullable=True),
        sa.Column('eng_ball', sa.SmallInteger, nullable=True),
        sa.Column('eng_pt_name', sa.String(255), nullable=True),
        sa.Column('eng_pt_reg_name', sa.String(255), nullable=True),
        sa.Column('eng_pt_area_name', sa.String(255), nullable=True),
        sa.Column('eng_pt_ter_name', sa.String(255), nullable=True),
        sa.Column('fra_test', sa.String(255), nullable=True),
        sa.Column('fra_test_status', sa.String(255), nullable=True),
        sa.Column('fra_ball100', sa.DECIMAL, nullable=True),
        sa.Column('fra_ball12', sa.SmallInteger, nullable=True),
        sa.Column('fra_dpa_level', sa.String(255), nullable=True),
        sa.Column('fra_ball', sa.SmallInteger, nullable=True),
        sa.Column('fra_pt_name', sa.String(255), nullable=True),
        sa.Column('fra_pt_reg_name', sa.String(255), nullable=True),
        sa.Column('fra_pt_area_name', sa.String(255), nullable=True),
        sa.Column('fra_pt_ter_name', sa.String(255), nullable=True),
        sa.Column('deu_test', sa.String(255), nullable=True),
        sa.Column('deu_test_status', sa.String(255), nullable=True),
        sa.Column('deu_ball100', sa.DECIMAL, nullable=True),
        sa.Column('deu_ball12', sa.SmallInteger, nullable=True),
        sa.Column('deu_dpa_level', sa.String(255), nullable=True),
        sa.Column('deu_ball', sa.SmallInteger, nullable=True),
        sa.Column('deu_pt_name', sa.String(255), nullable=True),
        sa.Column('deu_pt_reg_name', sa.String(255), nullable=True),
        sa.Column('deu_pt_area_name', sa.String(255), nullable=True),
        sa.Column('deu_pt_ter_name', sa.String(255), nullable=True),
        sa.Column('spa_test', sa.String(255), nullable=True),
        sa.Column('spa_test_status', sa.String(255), nullable=True),
        sa.Column('spa_ball100', sa.DECIMAL, nullable=True),
        sa.Column('spa_ball12', sa.SmallInteger, nullable=True),
        sa.Column('spa_dpa_level', sa.String(255), nullable=True),
        sa.Column('spa_ball', sa.SmallInteger, nullable=True),
        sa.Column('spa_pt_name', sa.String(255), nullable=True),
        sa.Column('spa_pt_reg_name', sa.String(255), nullable=True),
        sa.Column('spa_pt_area_name', sa.String(255), nullable=True),
        sa.Column('spa_pt_ter_name', sa.String(255), nullable=True),
        sa.Column('year_of_attempt', sa.SmallInteger, nullable=True)
    )


def downgrade() -> None:
    op.drop_table("funnel_status")
    op.drop_table('zno')
