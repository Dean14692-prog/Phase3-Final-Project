import click
from database import engine, Base, SessionLocal
from models import User, Note, Tag, NoteTag, Complaint
from datetime import datetime

@click.group()
def cli():
    pass

@cli.command('initialize')
def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    click.echo("Database initialized.")

@cli.command('update-db')
def seed_db():
    session = SessionLocal()

    user1 = User(username='alice', email='alice@example.com', password_hash='hashed_pwd', created_at=datetime.now())
    user2 = User(username='bob', email='bob@example.com', password_hash='hashed_pwd', created_at=datetime.now())
    session.add_all([user1, user2])
    session.commit()

    note1 = Note(user_id=user1.id, title='Note 1', content='Content of Note 1', created_at=datetime.now())
    note2 = Note(user_id=user2.id, title='Note 2', content='Content of Note 2', created_at=datetime.now())
    session.add_all([note1, note2])
    session.commit()

    tag1 = Tag(tag_name='urgent')
    tag2 = Tag(tag_name='personal')
    session.add_all([tag1, tag2])
    session.commit()

    note_tag1 = NoteTag(note_id=note1.id, tag_id=tag1.id)
    note_tag2 = NoteTag(note_id=note2.id, tag_id=tag2.id)
    session.add_all([note_tag1, note_tag2])
    session.commit()

    complaint1 = Complaint(user_id=user1.id, content='Complaint from Alice', created_at=datetime.now())
    complaint2 = Complaint(user_id=user2.id, content='Complaint from Bob', created_at=datetime.now())
    session.add_all([complaint1, complaint2])
    session.commit()

    session.close()
    click.echo("Database seeded with sample data.")

@cli.command('list-data')
@click.option('--table', type=click.Choice(['users', 'notes', 'tags', 'complaints', 'detailed_notes']), prompt='Which table to display?')
def list_data(table):
    session = SessionLocal()
    try:
        if table == 'users':
            users = session.query(User).all()
            if users:
                # Print a header
                click.secho(f"{'ID':<5} {'Username':<15} {'Email':<25} {'Created At':<25}", fg='cyan', bold=True)
                click.secho('-' * 80, fg='cyan')
                # Print user rows
                for user in users:
                    click.echo(f"{user.id:<5} {user.username:<15} {user.email:<25} {str(user.created_at):<25}")
                # Summary
                click.secho('-' * 80, fg='cyan')
                click.secho(f"Total users: {len(users)}", fg='green', bold=True)
            else:
                click.secho("No users found.", fg='yellow')

        # (You can similarly improve 'notes', 'tags', etc.)

        else:
            click.secho("Invalid table selected.", fg='red')

    except Exception as e:
        click.secho(f"An error occurred: {e}", fg='red')
        session.rollback()

    finally:
        session.close()


if __name__ == '__main__':
    cli()
