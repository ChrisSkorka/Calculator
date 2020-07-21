# built ins and libraries
import math, pyperclip, os, re, sys
from decimal import Decimal
from functools import reduce
from itertools import product
from datetime import datetime, date, time

# make scripts in folders importable
sys.path.append('\\Classes\\')
sys.path.append('\\BuiltIns\\')
sys.path.append('\\Parse\\')

# this
from Classes.built_ins import *
from Classes.data_structures import *
from Classes.data_types import *
from Classes.evaluable_tree_nodes import *
from Classes.token_matching import *
from Classes.token_tree_nodes import *
from BuiltIns.functions import *
from BuiltIns.groups import *
from BuiltIns.operations import *
from BuiltIns.seperators import *
from BuiltIns.variables import *
from BuiltIns.ConversionSpecifiers.distance import *
from BuiltIns.ConversionSpecifiers.area import *
from BuiltIns.ConversionSpecifiers.volume import *
from BuiltIns.ConversionSpecifiers.time import *
from Parse.lexing import *
from Parse.treeify import *
from calculate import *
from environment import *
from evaluate import *
from tokens import *



e = create_base_environment()
calc('1', e)