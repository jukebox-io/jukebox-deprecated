import logging
import os.path

import uvicorn

# Start Development Server (Uvicorn with Auto Reload Turned-on)
if __name__ == '__main__':
    # Configure and Run Uvicorn Server
    uvicorn.run(
        app='pxm.base:router',
        host='localhost',
        port=9090,
        reload=True,  # The `reload` and `workers` parameters are mutually exclusive.
        reload_dirs=os.path.dirname(__file__),
        log_level=logging.INFO,
    )
