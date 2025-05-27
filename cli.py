import click
from database import engine, Base, SessionLocal
from models import User, Note, Tag, NoteTag, Complaint
from datetime import datetime

@click.group()
def cli():
    pass

@cli.command('init-db')
def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    click.echo("Database initialized.")

@cli.command('seed-db')
def seed_db():
    session = SessionLocal()

    user1 = User(username='alice', email='alice@example.com', password_hash='hashed_pwd', created_at=datetime.utcnow())
    user2 = User(username='bob', email='bob@example.com', password_hash='hashed_pwd', created_at=datetime.utcnow())
    session.add_all([user1, user2])
    session.commit()

    note1 = Note(user_id=user1.id, title='Note 1', content='Content of Note 1', created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    note2 = Note(user_id=user2.id, title='Note 2', content='Content of Note 2', created_at=datetime.utcnow(), updated_at=datetime.utcnow())
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

    complaint1 = Complaint(user_id=user1.id, content='Complaint from Alice', created_at=datetime.utcnow())
    complaint2 = Complaint(user_id=user2.id, content='Complaint from Bob', created_at=datetime.utcnow())
    session.add_all([complaint1, complaint2])
    session.commit()

    session.close()
    click.echo("Database seeded with sample data.")

@cli.command('list-data')
@click.option('--table', type=click.Choice(['users', 'notes', 'tags', 'complaints', 'detailed_notes']), prompt='Which table to display?')
def list_data(table):
    session = SessionLocal()

    if table == 'users':
        users = session.query(User).all()
        for user in users:
            click.echo(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Created: {user.created_at}")

    elif table == 'notes':
        notes = session.query(Note).all()
        for note in notes:
            click.echo(f"ID: {note.id}, Title: {note.title}, UserID: {note.user_id}, Created: {note.created_at}")

    elif table == 'tags':
        tags = session.query(Tag).all()
        for tag in tags:
            click.echo(f"ID: {tag.id}, Tag: {tag.tag_name}")

    elif table == 'complaints':
        complaints = session.query(Complaint).all()
        for c in complaints:
            click.echo(f"ID: {c.id}, UserID: {c.user_id}, Content: {c.content}")

    elif table == 'detailed_notes':
        notes = session.query(Note).all()
        for note in notes:
            user = session.query(User).filter(User.id == note.user_id).first()
            tags = session.query(Tag).join(NoteTag, Tag.id == NoteTag.tag_id).filter(NoteTag.note_id == note.id).all()
            tag_names = ', '.join([tag.tag_name for tag in tags]) if tags else 'No Tags'

            click.echo(f"\nNote ID: {note.id}")
            click.echo(f"Title: {note.title}")
            click.echo(f"Content: {note.content}")
            click.echo(f"User: {user.username} ({user.email})")
            click.echo(f"Tags: {tag_names}")
            click.echo(f"Created: {note.created_at}, Updated: {note.updated_at}")

    else:
        click.echo("Invalid table.")

    session.close()
