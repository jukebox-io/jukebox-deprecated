# Configure Development Server (Uvicorn with Auto Reload Turned-on)

import logging
import os.path

import uvicorn

# Start the development server
if __name__ == '__main__':
    # To run directly from within a Python program, you should use uvicorn.run(app, **config)
    # Refer to, https://www.uvicorn.org/deployment/#running-programmatically

    uvicorn.run(
        # Application
        app='pxm.base:router',

        # Socket Binding
        host='localhost',  # serve on localhost ip addr
        port=8080,

        # Development
        reload=True,  # The `reload` and `workers` parameters are mutually exclusive.
        reload_dirs=os.path.dirname(__file__),

        # Logging
        log_level=logging.INFO,
    )
