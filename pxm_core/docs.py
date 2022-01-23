from fastapi.responses import HTMLResponse


def get_rapidoc_html(
        *,
        openapi_url: str,
        title: str,
        rapidoc_js_url: str = "https://cdn.jsdelivr.net/npm/rapidoc@9.1.3/dist/rapidoc-min.js",
        rapidoc_favicon_url: str = None,
        with_google_fonts: bool = True,
) -> HTMLResponse:
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>{title}</title>
        <!-- needed for adaptive design -->
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, minimum-scale=1, initial-scale=1, user-scalable=yes">
        """
    if with_google_fonts:
        html += """<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;600&family=Roboto+Mono
        &display=swap" rel="stylesheet"> """
    if rapidoc_favicon_url:
        html += """
        <link rel="shortcut icon" href="{rapidoc_favicon_url}">
        """
    html += f"""
        <style>
            rapi-doc{{
                width:100%;
            }}
        </style>
        <script type="module" src="{rapidoc_js_url}"></script>
        </head>
        <body>
        <rapi-doc
            allow-authentication = "true" 
            allow-search = "true"
            show-info = "true"
            spec-url = "{openapi_url}"
            theme = "light"
            show-header = "false" 
            render-style = "read"
            allow-try = "true"
            regular-font = "Open Sans"
            mono-font = "Roboto Mono"
            schema-style = "table"
        >
        </rapi-doc>
        </body>
        </html>
        """
    return HTMLResponse(html)
