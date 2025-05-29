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
    click.secho("\nDatabase initialized successfully!",fg="blue", bold=True)

@cli.command('seed-db')
def seed_db():
    session = SessionLocal()

    user1 = User(username='Martin Kioko', email='martin.kioko@example.com', password='martin_123', created_at=datetime.now())
    user2 = User(username='Dennis Ngui', email='dennis.ngui@example.com', password='dennis_123', created_at=datetime.now())
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
    tag5 = Tag(tag_name='testing')
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
    click.secho("\nDatabase seeded with sample data!", fg="blue", bold=True)

@cli.command('list-data')
@click.option('--table', 
              type=click.Choice(['users', 'notes', 'tags', 'complaints']), 
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


@cli.command('add-to-db')
def update_data():
    session = SessionLocal()
    table = input("Enter table name (users, notes, tags, complaints): ").strip().lower()

    if table == 'users':
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        new_user = User(username=username, email=email, password=password)
        session.add(new_user)

    elif table == 'notes':
        title = input("Enter title: ")
        content = input("Enter content: ")
        user_id = int(input("Enter user ID: "))
        new_note = Note(title=title, content=content, user_id=user_id)
        session.add(new_note)

    elif table == 'tags':
        tag_name = input("Enter tag name: ")
        new_tag = Tag(tag_name=tag_name)
        session.add(new_tag)

    elif table == 'complaints':
        user_id = int(input("Enter user ID: "))
        content = input("Enter complaint content: ")
        new_complaint = Complaint(user_id=user_id, content=content)
        session.add(new_complaint)

    else:
        print("\nInvalid table name")
        session.close()
        return

    session.commit()
    click.secho(f"\nNew entry added to {table} table!", fg = 'blue', bold = True)
    session.close()


@cli.command('delete-from-db')
def delete_data():
    session = SessionLocal()
    table = input("Enter table name to delete from (users, notes, tags, complaints): ").strip().lower()

    model = {
        'users': User,
        'notes': Note,
        'tags': Tag,
        'complaints': Complaint,
    }
    
    if table not in model:
        click.secho("\nInvalid table name", fg='red', bold = True)
        session.close()
        return
    
    try:
        record_id = int(input("Enter the ID of the record to delete: "))
    except ValueError:
        click.secho("\nInvalid ID. Must be an integer.", fg='red' ,bold = True)
        session.close()
        return
    record = session.query(model[table]).filter(model[table].id == record_id).first()
    
    if not record:
        click.secho(f"\nNo record found in {table} with ID {record_id}", fg='red', bold = True)
        session.close()
        return
    
    session.delete(record)
    session.commit()
    click.secho(f"\nRecord with ID {record_id} deleted from {table} successfully!", fg='green', bold=True)
    session.close()

@cli.command('update-record')
def update_record():
    # """Update a record in the database"""
    session = SessionLocal()

    # Map table names to models
    tables = {
        'users': User,
        'notes': Note,
        'tags': Tag,
        'complaints': Complaint,
    }

    # Ask for table name
    table_name = input("Enter table name (users, notes, tags, complaints): ").strip().lower()

    if table_name not in tables:
        click.secho("Invalid table name.", fg = 'red', bold = True)
        session.close()
        return

    model = tables[table_name]

    # Ask for record ID
    try:
        record_id = int(input("Enter record ID to update: "))
    except ValueError:
        click.secho("Invalid ID.", fg = 'red', bold = True)
        session.close()
        return

    # Find the record
    record = session.query(model).filter(model.id == record_id).first()

    if not record:
        click.secho(f"No record found with ID {record_id}.", fg = 'red', bold = True)
        session.close()
        return

    # Ask which field to update
    field_name = input("Enter field name to update: ").strip()

    # Check if the field exists
    if not hasattr(record, field_name):
        click.secho(f"Field '{field_name}' not found in {table_name}.", fg = 'red', bold = True)
        session.close()
        return

    # Ask for new value
    new_value = input(f"Enter new value for {field_name}: ")

    # Update the field
    setattr(record, field_name, new_value)

    # Save changes
    session.commit()
    print(f"Record with ID {record_id} updated successfully in {table_name} table.")
    session.close()

if __name__ == '__main__':
    cli()
