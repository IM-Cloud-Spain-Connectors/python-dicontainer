# Python DIContainer

[![Test](https://github.com/othercodes/python-dicontainer/actions/workflows/test.yml/badge.svg)](https://github.com/othercodes/python-dicontainer/actions/workflows/test.yml)

Provides the DIContainer interface along with a default implementation based in PInject Google Project.

## Installation

The easiest way to install DIContainer is to get the latest version from PyPI:

```bash
# using poetry
poetry add rndi-dicontainer
# using pip
pip install rndi-dicontainer
```

## The Contracts

This package provides two contracts or interfaces: `DIContainer` and `ServiceProvider`.

### DIContainer

```python
class DIContainer(ABC):
    @abstractmethod
    def get(self, cls: Type) -> Any:
        """
        Instantiate the given cls injecting the required dependencies.

        :param cls: Type The class name to instantiate.
        :raise DependencyBuildingFailure: Raised if there are no available dependency to inject.
        :raise InvalidClassType: Raised if the required class is not a valid Class Name. 
        :return: Any A valid instance of the given class type.
        """
```

The DIContainer expose one single method `get` that will accept a class name as argument and will return the same class
properly instantiated.

```python
container = Container()

instance = container.get(SomeClass)
```

### Service Provider

```python
class ServiceProvider(ABC):
    @abstractmethod
    def register(self):
        """
        Place to execute the explicit binding of your service.

        def register(self):
            self.bind_instance('foo', 'foo')
            self.bind_class('cache', RedisCache)

        The available binding methods are:

        self.bind_class(self, keyword, concretion)
            Define a dependency binding between a key to a class.
            > dependencies.to_class('request_builder', RequestBuilder)

        self.bind_instance(self, keyword, concretion)
            Define a dependency binding the dependency key to a certain instance.
            > dependencies.to_class('service_api_key', 'some_api_key')

        :return: None
        """

    @abstractmethod
    def bind_class(self, keyword: str, concrete: Any) -> ServiceProvider:
        """
        Binds the given keyword to the given class concretion. Each time someone
        requires the bounded keyword a new instance of the provided class will be
        injected.

        :param keyword: str The keyword to bind.
        :param concrete: Any The concrete class to instantiate and inject on requesting the keyword.
        :return: None
        """

    @abstractmethod
    def bind_instance(self, keyword: str, concrete: Any) -> ServiceProvider:
        """
        Binds the given keyword to the given instance concretion. Each time someone
        requires the bounded keyword the same instance will be providede.

        :param keyword: str The keyword to bind.
        :param concrete: Any The concrete instance to inject on requesting the keyword.
        :return: None
        """


```

A service provider allows you to register the dependencies into the dependency container as bindings. Each service
provider can provide multiple dependency definitions.

The `register` method allows you to register any dependency using the `bind_instance` and `bind_class` methods. In
addition, you can declare any `provide_` method to compose complex dependencies.

```python
from cache_interface.contracts import Cache
from cache_sqlite.adapter import SQLiteCacheAdapter
from rndi.dicontainer.adapter import Container, ServiceProvider
from service.shared.infrastructure import OAuthAutenticator, RESTAPIClient


class MainServiceProvider(ServiceProvider):
    def register(self):
        self.bind_instance('api_url', 'https://some.api.com/api/v1/')
        self.bind_instance('config', {
            'CACHE_DIR': '/tmp/cache',
            'CACHE_TTL': '900',
            'CACHE_SQLITE_NAME': 'cache',
        })
        # Requires OAuthAuthenticator and Cache implementation. 
        self.bind_class('api_client', RESTAPIClient)

    def provide_cache(self, config: dict) -> Cache:
        return SQLiteCacheAdapter(
            directory_path=config.get('CACHE_DIR', '/tmp/cache'),
            ttl=config.get('CACHE_TTL', 900),
            name=config.get('CACHE_SQLITE_NAME', 'cache'),
        )


container = Container([MainServiceProvider()])
```

Once the container is instantiated with service provider you can request any class that requires the
configured dependencies.

For more information please check https://github.com/google/pinject.
