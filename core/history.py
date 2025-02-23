from database.database import Database
from core.vars import ServiceVariables

def write_to_history(db: Database, result: str, chances: str):
    db.write_to_history(
        result=result,
        chances=chances
    )
    db.shrink_history()

def get_history(db: Database) -> str:

    history_start = """
            <table class="table">
                <thead>
                  <tr>
                    <th>Дата и время события</th>
                    <th>Результат</th>
                    <th>Шансы при броске</th>
                  </tr>
                </thead>
                <tbody>"""

    history_end = """
                </tbody>
            </table>"""

    history = history_start

    db_result = db.get_history()
    for row in db_result:
        history = history + f"""
        <tr>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td><center>{row[3]}</center></td>
        </tr>"""

    if len(db_result) < int(ServiceVariables.SHRINK_HISTORY_TO):
        we_have_to_add_placeholders = int(ServiceVariables.SHRINK_HISTORY_TO) - len(db_result)

        while we_have_to_add_placeholders > 0:
            history = history + f"""
            <tr>
                <td>...</td>
                <td>...</td>
                <td><center>...</center></td>
            </tr>"""
            we_have_to_add_placeholders = we_have_to_add_placeholders - 1

    history = history + history_end

    return history