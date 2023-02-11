from models import db, Script
from playhouse.migrate import migrate, SqliteMigrator
from playhouse.sqlite_ext import JSONField

migrator = SqliteMigrator(db)

if db.is_closed():
    db.connect()


initialization_params = JSONField(default=dict)
migrate(
    migrator.add_column(Script._meta.table_name, 'initialization_params',
                        initialization_params),
)
db.close()
