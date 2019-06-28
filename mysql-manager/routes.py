from handlers.mysql_handler import MysqlInstallHandler, MysqlListHandler, MysqlStartHandler, MysqlStopHandler, \
    MysqlRestartHandler, MysqlDeleteHandler, MysqlSearchHandler, MysqlBackupHandler, MysqlContainerInstallHandler
from handlers.server_handler import ServerRegisteHandler, ServerListHandler, ServerDeleteHandler
from handlers.admin_handler import LoginHandler, RegisteHandler
from handlers.task_handler import TaskRegisteHandler, TaskListHandler,  TaskDeleteHandler, TaskStartHandler, TaskStopHandler

handlers = [
    (r"/api/v1/server/registe", ServerRegisteHandler),
    (r"/api/v1/server/list", ServerListHandler),
    (r"/api/v1/server/delete", ServerDeleteHandler),

    (r"/api/v1/mysql/install", MysqlInstallHandler),
    (r"/api/v1/mysql_container/install", MysqlContainerInstallHandler),
    (r"/api/v1/mysql/list", MysqlListHandler),
    (r"/api/v1/mysql/search", MysqlSearchHandler),
    (r"/api/v1/mysql/start", MysqlStartHandler),
    (r"/api/v1/mysql/stop", MysqlStopHandler),
    (r"/api/v1/mysql/restart", MysqlRestartHandler),
    (r"/api/v1/mysql/delete", MysqlDeleteHandler),
    (r"/api/v1/mysql/backup", MysqlBackupHandler),

    (r"/api/v1/task/list", TaskListHandler),
    (r"/api/v1/task/registe", TaskRegisteHandler),
    (r"/api/v1/task/start", TaskStartHandler),
    (r"/api/v1/task/stop", TaskStopHandler),
    (r"/api/v1/task/delete", TaskDeleteHandler),

    (r"/api/v1/login", LoginHandler),
    (r"/api/v1/registe", RegisteHandler),
]
