"""empty message

Revision ID: 1548d804e208
Revises: 
Create Date: 2020-03-29 22:13:08.322215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1548d804e208'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cname', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('mobile', sa.String(length=11), nullable=False),
    sa.Column('addr', sa.String(length=255), nullable=True),
    sa.Column('real_name', sa.String(length=32), nullable=True),
    sa.Column('id_card', sa.String(length=18), nullable=True),
    sa.Column('avatar_url', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mobile'),
    sa.UniqueConstraint('name')
    )
    op.create_table('goods',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('counts', sa.Integer(), nullable=True),
    sa.Column('is_sell', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('index_image_url', sa.String(length=256), nullable=True),
    sa.Column('click_counts', sa.Integer(), nullable=True),
    sa.Column('cid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cid'], ['category.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('total_money', sa.Float(), nullable=True),
    sa.Column('ordertime', sa.DateTime(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.String(length=50), nullable=False),
    sa.Column('addr', sa.String(length=255), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('order_last_time', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('cdate', sa.DateTime(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.Column('gid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['gid'], ['goods.id'], ),
    sa.ForeignKeyConstraint(['uid'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shop_cart',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sdate', sa.DateTime(), nullable=True),
    sa.Column('counts', sa.Integer(), nullable=True),
    sa.Column('subTotal', sa.Float(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('gid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gid'], ['goods.id'], ),
    sa.ForeignKeyConstraint(['uid'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shop_cart')
    op.drop_table('comment')
    op.drop_table('order')
    op.drop_table('goods')
    op.drop_table('user')
    op.drop_table('category')
    # ### end Alembic commands ###