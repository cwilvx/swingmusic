import json

from app.models.plugins import Plugin

from ..utils import SQLiteManager


def plugin_tuple_to_obj(plugin_tuple: tuple) -> Plugin:
    return Plugin(
        name=plugin_tuple[1],
        active=bool(plugin_tuple[3]),
        settings=json.loads(plugin_tuple[4]),
    )


class PluginsMethods:
    @classmethod
    def insert_plugin(cls, plugin: Plugin):
        """
        Inserts one plugin into the database
        """

        sql = """INSERT OR IGNORE INTO plugins(
            name,
            description,
            active,
            settings
            ) VALUES(?,?,?,?)
            """

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(
                sql,
                (
                    plugin.name,
                    plugin.description,
                    int(plugin.active),
                    json.dumps(plugin.settings),
                ),
            )
            lastrowid = cur.lastrowid

            return lastrowid


    @classmethod
    def get_all_plugins(cls):
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute("SELECT * FROM plugins")
            plugins = cur.fetchall()
            cur.close()

            if plugins is not None:
                return [plugin_tuple_to_obj(plugin) for plugin in plugins]

        return []

    @classmethod
    def plugin_set_active(cls, name: str, active: int):
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute("UPDATE plugins SET active=? WHERE name=?", (active, name))
            cur.close()

    @classmethod
    def update_plugin_settings(cls, plugin_name: str, settings: dict):
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(
                "UPDATE plugins SET settings=? WHERE name=?",
                (json.dumps(settings), plugin_name),
            )
            cur.close()

    @classmethod
    def get_plugin_by_name(cls, name: str):
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute("SELECT * FROM plugins WHERE name=?", (name,))
            plugin = cur.fetchone()
            cur.close()

            if plugin is not None:
                return plugin_tuple_to_obj(plugin)

        return None
