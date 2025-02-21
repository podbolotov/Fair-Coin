from core.vars import ServiceVariables

def get_flip_page_content(quote, side, generation_pool, head_chance, tail_chance, history):
    return f"""
        <html>
            <head>
                <title>Честная монетка</title>
                <link id="favicon" rel="icon" type="image/x-icon" href="static/favicon.ico">
            </head>
            <body>
                <center>
                <h1>Честная монетка</h1>
                <h3>{quote}</h3>
                <hr>
                <p>Бросок состоялся</p>
                <br/>
                <h1 style="background: black; color: white;">Результат: <b>{side}</b></h1>
                <br/>
                <details>
                    <summary>Пул генерации</summary>
                    <p>{generation_pool}</p>
                </details>
                <br/>
                <p><b>Шансы на следующий бросок</b></p>
                <table border="2">
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
                {history}
                <br/>
                <br/>
                <form action="{ServiceVariables.URL}">
                  <input type="submit" value="Вернуться назад" />
                </form>
                </center>
            </body>
        </html>
        """
