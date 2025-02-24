from core.vars import ServiceVariables

def get_core_page_template(inner):
    return f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Честная монетка</title>
                <link id="favicon" rel="icon" type="image/x-icon" href="static/favicon.ico">
            </head>
            <style>
            html {{
              font-family: Arial, sans-serif;
            }}
            body {{
              width: 800px;
              margin: auto;
            }}
            .status-label {{
              padding: 6pt;
            }}
            .button {{
              background-color: #000000;
              border: none;
              color: white;
              padding: 15px 32px;
              text-align: center;
              text-decoration: none;
              display: inline-block;
              font-size: 16px;
            }}
            .table {{
              width: 100%;
              border: 2px solid;
              padding: 6pt;
            }}
            td {{
              height: 1.5em;
              padding-left: 6pt;
              padding-right: 6pt;
              align: center;
            }}
            </style>
            <body>
                {inner}
            </body>
        </html>
        """
