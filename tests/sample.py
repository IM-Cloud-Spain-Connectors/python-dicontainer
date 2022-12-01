from rndi.dicontainer.adapter import BaseServiceProvider as ServiceProvider


class SampleWithMissingDependency:
    def __init__(self, missing_dependency: str):
        self.missing_dependency = missing_dependency


class Sample:
    def __init__(self, foo: str, bar: str, greeting: str):
        self.foo = foo
        self.bar = bar
        self.greeting = greeting


class SampleServiceProvider(ServiceProvider):
    FOO = 'This is a foo.'
    BAR = 'This is a bar.'
    GREETING_TPL = "Hello {name}!"
    NAME = 'Vicent'

    def register(self):
        self.bind_instance('name', self.NAME)
        self.bind_instance('foo', self.FOO)
        self.bind_instance('bar', self.BAR)
        self.bind_class('foobar', Sample)

    def provide_greeting(self, name: str) -> str:
        return self.GREETING_TPL.format(name=name)
