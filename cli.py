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
                click.secho(f"{'ID':<5} {'Username':<15} {'Email':<25} {'Created At':<25}", fg='cyan', bold=True)
                click.secho('-' * 80, fg='cyan')
                for user in users:
                    click.echo(f"{user.id:<5} {user.username:<15} {user.email:<25} {str(user.created_at):<25}")
                click.secho('-' * 80, fg='cyan')
                click.secho(f"Total users: {len(users)}", fg='green', bold=True)
            else:
                click.secho("No users found.", fg='yellow')

        elif table == 'notes':
            # Make sure Note is imported correctly
            try:
                notes = session.query(Note).all()
                if notes:
                    click.secho(f"{'ID':<5} {'Title':<20} {'UserID':<8} {'Created At':<25}", fg='cyan', bold=True)
                    click.secho('-' * 80, fg='cyan')
                    for note in notes:
                        click.echo(f"{note.id:<5} {note.title:<20} {note.user_id:<8} {str(note.created_at):<25}")
                    click.secho('-' * 80, fg='cyan')
                    click.secho(f"Total notes: {len(notes)}", fg='green', bold=True)
                else:
                    click.secho("No notes found.", fg='yellow')
            except Exception as e:
                click.secho(f"Error accessing 'notes': {e}", fg='red')

        elif table == 'tags':
            # Similarly ensure Tag is imported and used
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
            click.secho("Invalid table selected.", fg='red')

    except Exception as e:
        click.secho(f"An error occurred: {e}", fg='red')
        session.rollback()
    finally:
        session.close()



if __name__ == '__main__':
    cli()
