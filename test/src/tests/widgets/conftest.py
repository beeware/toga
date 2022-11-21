from pytest import fixture


@fixture
async def native(widget):
    return widget._impl.native
