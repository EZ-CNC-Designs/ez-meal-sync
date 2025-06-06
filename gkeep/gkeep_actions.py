import random
from pathlib import Path
import gkeepapi

class GKeepActions:
    """Actions to perform on Google Keep in regards to EZ Meal Sync."""
    def __init__(self, user_email, user_master_token, user_grocery_store,
                 current_meal_note_name, next_meal_note_name):

        # Create an instance of gkeepapi
        self.keep = gkeepapi.Keep()

        # Access the API
        self.keep.authenticate(email=user_email, master_token=user_master_token)
        self.sync = self.keep.sync()
        print("Access to Google Keep was granted.")

        # Standard note names
        self.user_grocery_store = user_grocery_store
        self.current_meal_note_name = current_meal_note_name
        self.next_meal_note_name = next_meal_note_name

        # Add all existing note titles to a list.
        self.gnote_titles = []
        self.all_gnotes = self.keep.all()
        for gnote in self.all_gnotes:
            self.gnote_titles.append(gnote.title)
    

    def create_gnote(self, note_names):
        """Verify notes have been created. If not, new note will be added."""
        # Check if the needed notes are created.
        for name in note_names:
            if name in self.gnote_titles:
                print(f"Found {name}.")

            # Create a note if not found.
            else:
                print(f"Did not find {name}.")
                make_note = self.keep.createList(title=name)
                make_note.pinned = True
                print(f"{name} has been added to Google Keep and pinned.")
                self.keep.sync()

            # If the note is trashed, restore it to the main screen.
            trashed_note = list(self.keep.find(query=name, trashed=True))
            if trashed_note:
                gnote_restore = trashed_note[0]
                gnote_restore.untrash()
                self.keep.sync()
                print(f"{name} has been restored from the trash.")

            # If the note is archived, restore to the main screen.
            archived_note = list(self.keep.find(query=name, archived=True))
            if archived_note:
                gnote_restore = archived_note[0]
                gnote_restore.archived = False
                self.keep.sync()
                print(f"{name} has been restored from the archive.")

            # If the note is unpinned, pin it.
            unpinned_note = list(self.keep.find(query=name, pinned=False))
            if unpinned_note:
                gnote_pinned = unpinned_note[0]
                gnote_pinned.pinned = True
                self.keep.sync()
                print(f"{name} has been pinned.")


    def delete_checked(self, note_name):
        """Delete checked items within selected notes."""
        access_gnote = self.keep.find(query=note_name)
        gnote = next(access_gnote)

        # Use getattr to safely access 'items'.
        for item in getattr(gnote, 'items', []):  # Default to an empty list if 'items' is missing.
            if item.checked:
                item.delete()
                print(f"Checked item, {item} have been removed from {note_name}.")
        self.keep.sync()
            

    def pull_note_content(self, note_name):
        """Pull all the information from the selected notes so it can be manipulated."""
        """Returns a list of note content."""
        note_contents = []
        # Find the note.
        access_gnote = self.keep.find(query=note_name)
        gnote = next(access_gnote)

        # Use getattr to safely access 'item' instead of 'gnote.item'.
        for item in getattr(gnote, 'items', []):  # Default to empty list if 'item' attribute is missing.
            note_contents.append(item.text)
        print(f"Contents have been pulled from {note_name}.")

        return note_contents
    

    def delete_contents(self, note_name):
        """Delete the note contents out of Google Keep."""
        access_note = self.keep.find(query=note_name)
        gnote = next(access_note)

        # Use getattr to safely access 'items'.
        for item in getattr(gnote, 'items', []):  # Default to empty list if 'items' is missing.
            if item:
                item.delete()
        self.keep.sync()
        print(f"Items within {note_name} have been removed.")
            

    def add_contents(self, note_name, contents_to_add):
        """Add contents to a specified Google Keep note."""
        access_note = self.keep.find(query=note_name)
        gnote = next(access_note)

        for content in contents_to_add:
            gnote.add(content)
        print(f"Contents have been added to {note_name}.")
        self.keep.sync()
