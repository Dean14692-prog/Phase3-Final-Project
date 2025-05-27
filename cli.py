import click
from database import engine, Base, SessionLocal
from models import User, Note, Tag, NoteTag, Complaint
from datetime import datetime

@click.group()
def cli():
    pass

@cli.command('initialize')
def initialize_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    click.echo("Database initialized.")

@cli.command('update-db')
def update_db():
    session = SessionLocal()

    user1 = User(username='Martin Kioko', email='martin.kioko@example.com', password_hash='martin_123', created_at=datetime.now())
    user2 = User(username='Dennis Ngui', email='dennis.ngui@example.com', password_hash='dennis_123', created_at=datetime.now())
    session.add_all([user1, user2])
    session.commit()

    note1 = Note(user_id=user1.id, title='Meeting', content='Site meeting in Mombasa', created_at=datetime.now())
    note2 = Note(user_id=user2.id, title='Shopping', content='Buy snacks for my baby', created_at=datetime.now())
    note3 = Note(user_id=user2.id, title='Family', content='Have a coffee date with my wife', created_at=datetime.now())
    note4 = Note(user_id=user2.id, title='Gym', content='Go to the gym over the weekend', created_at=datetime.now())

    session.add_all([note1, note2, note3, note4])
    session.commit()

    tag1 = Tag(tag_name='urgent')
    tag2 = Tag(tag_name='personal')
    tag3 = Tag(tag_name='work')
    tag4 = Tag(tag_name='family')
    session.add_all([tag1, tag2, tag3, tag4])
    session.commit()

    note_tag1 = NoteTag(note_id=note1.id, tag_id=tag1.id)
    note_tag2 = NoteTag(note_id=note2.id, tag_id=tag2.id)
    note_tag3 = NoteTag(note_id=note3.id, tag_id=tag3.id)
    note_tag4 = NoteTag(note_id=note4.id, tag_id=tag4.id)
    session.add_all([note_tag1, note_tag2, note_tag3, note_tag4])
    session.commit()

    complaint1 = Complaint(user_id=user1.id, content='Complaint from Martin Kioko', created_at=datetime.now())
    complaint2 = Complaint(user_id=user2.id, content='Complaint from Dennis Ngui', created_at=datetime.now())
    session.add_all([complaint1, complaint2])
    session.commit()

    session.close()
    click.echo("Database seeded with sample data.")

@cli.command('list-data')
@click.option('--table', 
              type=click.Choice(['users', 'notes', 'tags', 'complaints', 'detailed_notes']), 
              prompt='Which table to display?')
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
            tags = session.query(Tag).all()
            click.secho(f"{'ID':<5} {'Tag':<20}", fg='cyan', bold=True)  
            click.secho('-' * 30, fg='cyan')  
            for tag in tags:
                click.secho(f"{tag.id:<5} {tag.tag_name:<20}", fg='white')  
            click.secho('-' * 30, fg='cyan')
            click.secho(f"Total tags: {len(tags)}", fg='green', bold=True)  

        elif table == 'complaints':
            complaints = session.query(Complaint).all()
            
            click.secho(f"{'ID':<5} {'User ID':<10} {'Complaint':<60}", fg='cyan', bold=True)
            click.secho('-' * 80, fg='cyan')
            
            for c in complaints:
                content_preview = (c.content[:57] + '...') if len(c.content) > 60 else c.content
                click.echo(f"{c.id:<5} {c.user_id:<10} {content_preview:<60}")
            
            click.secho('-' * 80, fg='cyan')
            click.secho(f"Total complaints: {len(complaints)}", fg='green', bold=True)

        else:
            click.secho("Invalid table selected.", fg='red')

    except Exception as e:
        click.secho(f"An error occurred: {e}", fg='red')
        session.rollback()
    finally:
        session.close()


@cli.command('update-data')
def update_data():
    session = SessionLocal()



if __name__ == '__main__':
    cli()
