# Using `invoke` as library
# http://docs.pyinvoke.org/en/stable/concepts/library.html

from invoke import Collection, Program

from . import dev, docker, git, helm, py


namespace = Collection()
namespace.add_collection(dev)
namespace.add_collection(docker)
namespace.add_collection(git)
namespace.add_collection(helm)
namespace.add_collection(py)


program = Program(namespace=namespace, version="0.0.1a0")
