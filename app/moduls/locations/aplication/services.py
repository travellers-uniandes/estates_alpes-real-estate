from app.seedwork.aplication.services import Service
from ..aplication.dto import ListDTO
from app.moduls.locations.domain.factories import ListFactory
from app.moduls.locations.infrastructure.factories import RepositoryFactory
from ..domain.repositories import ListRepository
from .mappers import MapeadorLocation

class ListService(Service):

    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()
        self._list_factories: ListFactory = ListFactory()

    @property
    def repository_factory(self):
        return self._repository_factory

    @property
    def list_factory(self):
        return self._list_factories

    def get_all_list(self) -> ListDTO:
        repository = self.repository_factory.create_object(ListRepository.__class__)
        
        return self.list_factory.create_object(repository.get_all(), MapeadorLocation())
    
    def create(self, data):
        repository = self.repository_factory.create_object(ListRepository.__class__)
        
        return self.list_factory.create_object(repository.create(data), MapeadorLocation())