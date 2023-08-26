#  Copyright (c) 2023 JukeBox Developers - All Rights Reserved
#  This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
#  Please see the LICENSE file that should have been included as part of this package

from jukebox.database.migrations import perform_migrations

if __name__ == "__main__":
    # Run pending migrations (if any). Otherwise, re-apply the last migration
    perform_migrations(develop=True)
