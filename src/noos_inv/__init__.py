# Using `invoke` as a library
# http://docs.pyinvoke.org/en/stable/concepts/library.html

from importlib import metadata

from invoke import Collection, Config, Program

from . import docker, git, helm, local, python, terraform


__version__ = metadata.version("noos-inv")


class BaseConfig(Config):
    prefix = "noosinv"


ns = Collection()
ns.add_collection(docker.ns)
ns.add_collection(git.ns)
ns.add_collection(helm.ns)
ns.add_collection(local.ns)
ns.add_collection(python.ns)
ns.add_collection(terraform.ns)


main = Program(namespace=ns, config_class=BaseConfig, version=__version__)
