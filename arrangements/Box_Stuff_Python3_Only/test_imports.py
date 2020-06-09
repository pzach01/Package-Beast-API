
from . import single_pack
from . import py3dbp_main
from .py3dbp_main import ContainerPY3DBP,ItemPY3DBP,Packer
import random
# makes test deterministic (reproducable)
seed=random.randint(0,10000)
seed=7
print('Seed:'+str(seed))
random.seed(seed)




import itertools
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from . import box_stuff2


from . import single_pack
from . import testing_single_pack

from . import py3dbp_auxiliary_methods
from .py3dbp_auxiliary_methods import outside_container
