from core.vars import ServiceVariables
from content.core_page_template import get_core_page_template

def get_main_page_content(quote, head_chance, tail_chance, history):
    main_page = f"""
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
    {history}
    <br/>
    <form action="{ServiceVariables.URL}/flip">
      <input class="button" type="submit" value="Бросить монетку" />
    </form>
    <br/>
    </center>
    """
    return get_core_page_template(inner=main_page)
