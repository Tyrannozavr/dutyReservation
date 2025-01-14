from db.queries.duty import duty_queries
from services.duty import DutiesServices

duty_services = DutiesServices(queries=duty_queries)