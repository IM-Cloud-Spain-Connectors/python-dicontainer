#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Type


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
