from core.vars import ServiceVariables
from content.core_page_template import get_core_page_template


def get_main_page_content(quote, last_result, head_chance, tail_chance, history):
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
            <center>
            <h1>Честная монетка</h1>
            <h3>{quote}</h3>
            <hr>
            <p>Если тебе выпала не та сторона, которую ты хотел - шансы изменятся в твою пользу.</p>
            <section id="flip_status_label"><h1 id='result-text' class='status-label' style='background: black; color: white;'>Последний результат: {last_result}</b></h1></section>
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
                <td id="head_chance_label"><center>{head_chance}%</center></td>
                <td id="tail_chance_label"><center>{tail_chance}%</center></td>
              </tr>
            </tbody>
            </table>
            <br/>
            <details id="chances_reset_container">
                <summary>Сбросить шансы можно тут</summary>
                <br/>
                <p>Нажатие на кнопку "Сбросить шансы" вернёт шансы к значениям 50 на 50.<br/>Не злоупотребляйте!</p>
                <form action="" onsubmit="closeResetDetails(); sendAction(event, 'reset')">
                  <input class="button" type="submit" value="Сбросить шансы" />
                </form>
                <br/>
            </details>
            <br/>
            <section id="history_section">
            {history}
            </section>
            <br/>
            <form action="" onsubmit="sendAction(event, 'flip')">
              <input class="button" type="submit" value="Бросить монетку" />
            </form>
            <br/>
            </center>

            <script>
                var ws = new WebSocket("ws://{ServiceVariables.URL}/ws");
                
                function addWebSocketActions() {{
                
                    ws.onmessage = function(event) {{
                        event_data = JSON.parse(event.data)
                        console.log(event_data.message)
                        
                        if (event_data.message === 'coin_flip_response') {{
                          var flip_status_label = document.getElementById('flip_status_label');
                          var result_text = event_data.payload.result;
                          flip_status_label.innerHTML = "<h1 id='result-text' class='status-label' style='background: black; color: white;'>"
                          + 'Последний результат: ' + result_text + '</b></h1>'
                        
                          var head_chance_label = document.getElementById('head_chance_label')
                          head_chance_label.innerHTML = "<center>" + event_data.payload.new_head_chance + "%</center>"
                          
                          var head_chance_label = document.getElementById('tail_chance_label')
                          head_chance_label.innerHTML = "<center>" + event_data.payload.new_tail_chance + "%</center>"
                          
                          var history_section = document.getElementById('history_section')
                          history_section.innerHTML = event_data.payload.history
                        }};
                        
                        if (event_data.message === 'chances_reset_response') {{
                          var flip_status_label = document.getElementById('flip_status_label');
                          var result_text = event_data.payload.result;
                          flip_status_label.innerHTML = "<h1 id='result-text' class='status-label' style='background: black; color: white;'>"
                          + 'Последний результат: ' + result_text + '</b></h1>'
                        
                          var head_chance_label = document.getElementById('head_chance_label')
                          head_chance_label.innerHTML = "<center>" + event_data.payload.new_head_chance + "%</center>"
                          
                          var head_chance_label = document.getElementById('tail_chance_label')
                          head_chance_label.innerHTML = "<center>" + event_data.payload.new_tail_chance + "%</center>"
                          
                          var history_section = document.getElementById('history_section')
                          history_section.innerHTML = event_data.payload.history
                          
                          var deet = document.getElementById('chances_reset_container');
                          deet.open = false;
                        }};
                        
                        if (event_data.message === 'repeat_last_for_you_only_response') {{
                          var flip_status_label = document.getElementById('flip_status_label');
                          var result_text = event_data.payload.result;
                          flip_status_label.innerHTML = "<h1 id='result-text' class='status-label' style='background: black; color: white;'>"
                          + 'Последний результат: ' + result_text + '</b></h1>'
                        
                          var head_chance_label = document.getElementById('head_chance_label')
                          head_chance_label.innerHTML = "<center>" + event_data.payload.new_head_chance + "%</center>"
                          
                          var head_chance_label = document.getElementById('tail_chance_label')
                          head_chance_label.innerHTML = "<center>" + event_data.payload.new_tail_chance + "%</center>"
                          
                          var history_section = document.getElementById('history_section')
                          history_section.innerHTML = event_data.payload.history
                          
                          var deet = document.getElementById('chances_reset_container');
                          deet.open = false;
                        }};
                        
                    }};
                    
                    ws.onopen = function(event) {{
                        flip_status_label.innerHTML = "<h1 id='result-text' class='status-label' style='background: green; color: white;'>"
                        + 'Соединение восстановлено!' + '</b></h1>'
                        
                        setTimeout(ws.send('repeat_last_for_me_only'), 1000);
                    }};
                
                }};
                
                addWebSocketActions();
                
                function sendAction(event, action = 'flip') {{
                    var action_value = action
                    ws.send(action_value)
                    event.preventDefault()
                }};
                
                function closeResetDetails() {{
                    var details = document.getElementById('chances_reset_container');
                    details.open = false;
                }};
            
                var timeoutId = null;

                function checkWebSocketState() {{
                  if (ws.readyState === WebSocket.OPEN) {{
                    console.info("WS is OPEN");
                  }} else if (ws.readyState === WebSocket.CONNECTING) {{
                    console.info("WS is CONNECTING");
                  }} else {{
                    flip_status_label.innerHTML = "<h1 id='result-text' class='status-label' style='background: red; color: white;'>"
                    + 'Отсутствует соединение с сервером.</br>Пытаемся переподключиться...' + '</b></h1>'
                    ws = new WebSocket("ws://{ServiceVariables.URL}/ws");
                    addWebSocketActions();
                  }}
                  
                  timeoutId = setTimeout(checkWebSocketState, 1000);
                  
                }}
                
                checkWebSocketState();
                
            </script>
        </body>
    </html>
    """
    return main_page_content
    # return get_core_page_template(inner=main_page_content)
