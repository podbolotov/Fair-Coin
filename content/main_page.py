from core.vars import ServiceVariables
from content.core_page_template import get_core_page_template


def get_main_page_content(quote, head_chance, tail_chance, history):
    main_page_content = f"""
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
            <!-- <h1>WebSocket Chat</h1>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            <ul id='messages'>
            </ul> -->

            <center>
            <h1>Честная монетка</h1>
            <h3>{quote}</h3>
            <hr>
            <p>Если тебе выпала не та сторона, которую ты хотел - шансы изменятся в твою пользу.</p>
            <h1 id="waiting-text" class="status-label">Ожидание броска</b></h1>
            <p><b>Текущие шансы</b></p>
            <table class="table">
            <thead>
              <tr>
                <th>{ServiceVariables.CUSTOM_HEAD_LABEL}</th>
                <th>{ServiceVariables.CUSTOM_TAIL_LABEL}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><center>{head_chance}%</center></td>
                <td><center>{tail_chance}%</center></td>
              </tr>
            </tbody>
            </table>
            <br/>
            <details>
                <summary>Сбросить шансы можно тут</summary>
                <br/>
                <p>Нажатие на кнопку "Сбросить шансы" вернёт шансы к значениям 50 на 50.<br/>Не злоупотребляйте!</p>
                <form action="{ServiceVariables.URL}/reset">
                  <input class="button" type="submit" value="Сбросить шансы" />
                </form>
                <br/>
            </details>
            <br/>
            <section id="history_section">
            {history}
            </section>
            <br/>
            <form action="{ServiceVariables.URL}/flip">
              <input class="button" type="submit" value="Бросить монетку" />
            </form>
            <br/>
            </center>

            <script>
                var ws = new WebSocket("ws://{ServiceVariables.URL}/ws");
                ws.onmessage = function(event) {{
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                }};
                function sendMessage(event) {{
                    var input = document.getElementById("messageText")
                    ws.send(input.value)
                    input.value = ''
                    event.preventDefault()
                }};
            </script>
        </body>
    </html>
    """
    return main_page_content
    # return get_core_page_template(inner=main_page_content)
