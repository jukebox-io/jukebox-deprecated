import logging
import os.path

import uvicorn

from pxm.settings import PORT


# Start the development server (Uvicorn with Auto Reload Turned-on)
def main() -> None:
    # To run directly from within a Python program, you should use uvicorn.run(app, **config)
    uvicorn.run(

        # Application
        app='pxm.server:router',

        # Socket Binding
        host='localhost', port=PORT,  # serve on localhost ip address

        # Development
        reload=True,  # The `reload` and `workers` parameters are mutually exclusive.
        reload_dirs=os.path.dirname(__file__),

        # Logging
        log_level=logging.INFO,
    )


if __name__ == '__main__':
    main()
