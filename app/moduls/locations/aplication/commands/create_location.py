from app.seedwork.aplication.commands import Command
from app.moduls.locations.aplication.dto import ListDTO
from .base import CreateLocationBaseHandler
from dataclasses import dataclass, field
from app.seedwork.aplication.commands import execute_command as command

from app.moduls.locations.domain.entities import Location
from app.seedwork.infrastructure.uow import UnitOfWorkPort, UnitOfWorkPort1
from app.moduls.locations.aplication.mappers import MapeadorLocation
from app.moduls.locations.infrastructure.repositories import ListRepository

@dataclass
class CreateLocation(Command):
    locations: ListDTO

class CreateEstateHandler(CreateLocationBaseHandler):
    
    def handle(self, command: CreateLocation):
        locations = command
        
        location_list: ListDTO = self.list_factories.create_object(locations, MapeadorLocation())
        location_list.create_location(location_list)
        repository = self.repository_factory.create_object(ListRepository.__class__)

        UnitOfWorkPort1.regist_batch(repository.create, location_list)
        UnitOfWorkPort1.savepoint()
        UnitOfWorkPort1.commit()


@command.register(CreateLocation)
def execute_command_create_state(comando: CreateLocation):
    handler = CreateEstateHandler()
    handler.handle(comando)
    