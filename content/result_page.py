from content.core_page_template import get_core_page_template
from core.vars import ServiceVariables


def get_result_page_content(quote, side, generation_pool, head_chance, tail_chance, history):
    result_page = f"""
        <center>
        <h1>Честная монетка</h1>
        <h3>{quote}</h3>
        <hr>
        <p>Бросок состоялся</p>
        <h1 id="result-text" class="status-label" style="background: black; color: white;">Результат: {side}</h1>
        <p><b>Шансы на следующий бросок</b></p>
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
            <summary>Пул генерации</summary>
            <p>{generation_pool}</p>
        </details>
        <br/>
        {history}
        <br/>
        <form action="{ServiceVariables.URL}">
          <input class="button" type="submit" value="Вернуться назад" />
        </form>
        </center>
        """
    return get_core_page_template(inner=result_page)
