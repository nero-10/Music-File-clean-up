import os
import re
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TPE1

# Define the main folder path
main_folder_path = r"C:\Users\Nilay's PC\Music\Music"  # Replace with your actual path

# Walk through all folders and files within the main folder
for root, dirs, files in os.walk(main_folder_path):
    for filename in files:
        # Only process audio files (e.g., .mp3 files)
        if filename.lower().endswith('.mp3'):
            # Separate the file name from the extension
            name, ext = os.path.splitext(filename)

            # Attempt to load the file's metadata to get the Contributing Artist
            try:
                audio = MP3(os.path.join(root, filename), ID3=ID3)
                artist = audio.tags.get('TPE1', None)  # 'TPE1' is the ID3 tag for Contributing Artist
                if artist:
                    artist_name = artist.text[0]  # Get the artist's name from the tag

                    # Remove the artist's name if it's in the filename
                    name = re.sub(re.escape(artist_name), '', name, flags=re.IGNORECASE)

            except Exception as e:
                print(f"Could not read metadata for {filename}: {e}")
                artist_name = None

            # Remove leading numbers, dots, and text after "@" symbol
            new_name = re.sub(r'^[.\d]+[-_ ]?|@.*', '', name).strip()

            # Ensure the new name isn't empty and reattach the extension
            if new_name:
                new_name += ext
            else:
                # If new_name is empty, keep the original filename
                new_name = filename

            # Rename the file if the name has changed and the target name does not already exist
            old_file = os.path.join(root, filename)
            new_file = os.path.join(root, new_name)
            if new_name != filename and not os.path.exists(new_file):
                os.rename(old_file, new_file)
                print(f'Renamed: {filename} to {new_name} in {root}')
            elif new_name != filename:
                print(f"Skipping rename for {filename} to avoid conflict with existing file.")
