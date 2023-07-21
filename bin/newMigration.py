#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from jukebox.database.migrations import new_migration


if __name__ == '__main__':
    # Prompt for input
    title_input: str = input("Enter a suitable message for your migration: ")

    # Create a new migration script
    new_migration(title_input)
