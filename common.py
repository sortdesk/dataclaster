from dataclasses import Field, MISSING


class FieldWithConfig(Field):
    def __init__(self, config, *args, **kwargs) -> None:
        self.config = config
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        repr = super().__repr__()
        return f"{repr[:-1]},config={self.config!r})"


def fieldwrapper(*, config, default=MISSING, default_factory=MISSING, init=True,
                 repr=True, hash=None, compare=True, metadata=None):

    if default is not MISSING and default_factory is not MISSING:
        raise ValueError("cannot specify both default and default_factory")
    return FieldWithConfig(config, default, default_factory, init, repr, hash, compare, metadata)
