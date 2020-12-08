# Using `invoke` as library
# http://docs.pyinvoke.org/en/stable/concepts/library.html

from invoke import Collection, Config, Program

from . import docker, git, helm, local, python


__version__ = "0.0.1a5"


class BaseConfig(Config):
    prefix = "noosci"


ns = Collection()
ns.add_collection(docker.ns)
ns.add_collection(git.ns)
ns.add_collection(helm.ns)
ns.add_collection(local)
ns.add_collection(python.ns)


main = Program(namespace=ns, config_class=BaseConfig, version=__version__)
