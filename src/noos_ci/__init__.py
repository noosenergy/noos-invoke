# Using `invoke` as library
# http://docs.pyinvoke.org/en/stable/concepts/library.html

from invoke import Collection, Config, Program

from . import dev, docker, git, helm, py


__version__ = "0.0.1a4"


class BaseConfig(Config):
    prefix = "noosci"


ns = Collection()
ns.add_collection(dev)
ns.add_collection(docker.ns)
ns.add_collection(git.ns)
ns.add_collection(helm.ns)
ns.add_collection(py.ns)


main = Program(namespace=ns, config_class=BaseConfig, version=__version__)
