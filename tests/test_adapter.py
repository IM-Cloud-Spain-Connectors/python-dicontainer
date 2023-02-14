import pytest
from rndi.dicontainer.adapter import Container
from rndi.dicontainer.exceptions import DependencyBuildingFailure, InvalidClassType
from tests.sample import Sample, SampleServiceProvider, SampleWithMissingDependency


def test_container_should_provide_required_instance_using_dependencies_from_service_provider():
    container = Container([SampleServiceProvider()])
    service = container.get(Sample)

    assert isinstance(service, Sample)
    assert service.foo == SampleServiceProvider.FOO
    assert service.bar == SampleServiceProvider.BAR
    assert service.greeting == SampleServiceProvider.GREETING_TPL.format(
        name=SampleServiceProvider.NAME,
    )


def test_container_should_raise_dependency_building_failure_on_missing_dependency():
    container = Container([SampleServiceProvider()])

    with pytest.raises(DependencyBuildingFailure):
        container.get(SampleWithMissingDependency)


def test_container_should_raise_invalid_class_type_on_calling_get_with_no_class_type():
    container = Container([])

    with pytest.raises(InvalidClassType):
        container.get(42)
