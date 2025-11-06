import sys
from typing import Tuple, List, Set, Dict, Union

import pytest


@pytest.fixture(params=[1, 2])
def new_style(request):
    return request.param


@pytest.fixture(params=[Dict, dict])
def dict_type(request):
    return request.param


@pytest.fixture(params=[List, list])
def list_type(request):
    return request.param


@pytest.fixture(params=[Tuple, tuple])
def tuple_type(request):
    return request.param


@pytest.fixture(params=[Set, set])
def set_type(request):
    return request.param


@pytest.fixture(params=[True, False])
def make_union(request):
    def function(first, second):
        if request.param:
            return first | second
        return Union[first, second]
    if request.param and sys.version_info < (3, 10):
        pytest.skip('This operation became available in Python 3.9')
    return function
