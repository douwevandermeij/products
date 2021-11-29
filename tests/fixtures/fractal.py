import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "context: overrides for adapters in Context")


def reset(fractal, settings):
    fractal.settings.reload(settings)
    fractal.context.reload()
    return fractal


@pytest.fixture(autouse=True)
def fractal(request):
    from app.service.main import ProductFractal as Fractal

    service = Fractal()

    marker = request.node.get_closest_marker("settings")
    if marker:
        return reset(service, marker.args[0])
    else:
        return reset(service, {})


@pytest.fixture
def reset_fractal(fractal):
    def _reset(settings):
        return reset(fractal, settings)

    return _reset
