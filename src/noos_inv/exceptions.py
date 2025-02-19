class ValidationError(Exception):
    """Error raised in validating context variables."""

    pass


class PathNotFound(ValidationError):
    """Error raised if a filesytem path isn't valid."""

    pass


class InvalidConfig(Exception):
    """Error raised in validating a config file schema."""

    pass
