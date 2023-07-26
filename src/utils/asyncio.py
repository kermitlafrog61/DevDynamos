async def await_awaitable_attrs(model):
    attrs = dir(model)
    for attr in attrs:
        if attr.startswith('__') and attr.endswith('__'):
            continue
        await getattr(model.awaitable_attrs, attr)
