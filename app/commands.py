import string
import random

import click
from flask.cli import AppGroup

from app import db
from app.models import User
from app.permissions import Role


roles_cli = AppGroup('roles', help='Manipulations with roles')


@roles_cli.command('create', help='Create new role')
@click.argument('name')
@click.argument('display_name')
def roles_create(name, display_name):
    if Role.query.filter(Role.name == name):
        click.echo('This Role name already in use', err=True)
        return
    r = Role(name, display_name)
    db.session.add(r)
    db.session.commit()


# @roles_cli.command('grant', help='Grant to passed role passed list of permissions')
# @click.argument('role')
# @click.argument('perms', nargs=-1)
# def roles_grant(role, perms):
#     r = Role.query.filter(Role.name == role).first()
#     if not r:
#         click.echo('Role not found', err=True)
#         return
#     for p_name in perms:
#         p = Permission.query.filter(Permission.name == p_name).first()
#         if not p:
#             click.echo(f'Permission {p_name} not found', err=True)
#             continue
#         r.permissions.append(p)
#     db.session.commit()
#     click.echo('Successful granted')
#
#
# @roles_cli.command('revoke', help='Revoke permissions from role')
# @click.argument('role')
# @click.argument('perms', nargs=-1)
# def roles_revoke(role, perms):
#     r = Role.query.filter(Role.name == role).first()
#     if not r:
#         click.echo('Role not found', err=True)
#         return
#     for p_name in perms:
#         p = r.permissions.filter(Permission.name == p_name).first()
#         if not p:
#             click.echo(f'Permission {p_name} not in role {role}', err=True)
#             continue
#         r.permissions.remove(p)
#     db.session.commit()


@roles_cli.command('list', help='Shows list of all roles')
def roles_list():
    roles = Role.query.all()
    for r in roles:
        click.echo(str(r))


@roles_cli.command('info', help='Shows info for passed role')
@click.argument('role')
def roles_info(role):
    r = Role.query.filter(Role.name == role).first()
    if not r:
        click.echo('Role not found', err=True)
        return
    click.echo(repr(r))
    click.echo('Available permissions:')
    for p in r.permissions.all():
        click.echo(str(p))


users_cli = AppGroup('users', help='Manipulations with users')


@users_cli.command('list', help='Shows list of all users')
def users_list():
    for u in User.query.all():
        click.echo(str(u))


@users_cli.command('roles', help='Shows user\'s roles')
@click.argument('user')
def users_roles(user):
    u = User.query.filter(User.username == user).first()
    if not u:
        click.echo('User not found', err=True)
        return
    for r in u.roles:
        click.echo(str(r))


@users_cli.command('create', help='Create new user')
@click.argument('username')
@click.argument('profile_name')
@click.option('-p', '--password', default=None, help='Set not random password')
@click.option('-l', '--length', default=12, help='Random password length')
def users_create(username, profile_name, password, length):
    if password is None:
        password = ''.join([random.choice(string.hexdigits) for _ in range(length)])
    u = User.new(username, profile_name, password)
    db.session.add(u)
    db.session.commit()
    click.echo(f'Created user {u} with temporary password: {password}')
