from core.vars import ServiceVariables

def get_main_page_content(quote, head_chance, tail_chance, history):
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
                <p>Если тебе выпала не та сторона, которую ты хотел - шансы изменятся в твою пользу.</p>
                <br/>
                <h1>Ожидание броска</b></h1>
                <br/>
                <p><b>Текущие шансы</b></p>
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
                <details>
                    <summary>Сбросить шансы можно тут</summary>
                    <br/>
                    <p>Нажатие на кнопку "Сбросить шансы" вернёт шансы к значениям 50 на 50.<br/>Не злоупотребляйте!</p>
                    <form action="{ServiceVariables.URL}/reset">
                      <input type="submit" value="Сбросить шансы" />
                    </form>
                    <br/>
                </details>
                <br/>
                {history}
                <br/>
                <br/>
                <form action="{ServiceVariables.URL}/flip">
                  <input type="submit" value="Бросить монетку" />
                </form>
                <br/>
                </center>
            </body>
        </html>
        """
