import lightgbm as lgb
import numpy as np
import pytest

import lleaves


def test_interface():
    lgbm = lgb.Booster(model_file="tests/models/tiniest_single_tree/model.txt")
    llvm = lleaves.Model("tests/models/tiniest_single_tree/model.txt")

    for arr in [np.array([1.0, 1.0, 1.0]), [1.0, 1.0, 1.0]]:
        with pytest.raises(ValueError) as err1:
            llvm.predict(arr)
        with pytest.raises(ValueError) as err2:
            lgbm.predict(arr)

        assert "2 dimensional" in err1.value.args[0]
        assert "2 dimensional" in err2.value.args[0]


@pytest.mark.parametrize(
    "model_file, n_args",
    [
        ("tests/models/pure_categorical/model.txt", 3),
        ("tests/models/tiniest_single_tree/model.txt", 3),
    ],
)
def test_input_dtypes(model_file, n_args):
    lgbm = lgb.Booster(model_file=model_file)
    llvm = lleaves.Model(model_file)

    arr = np.array([[1.0, 1.0, 1.0]], dtype=np.float32)
    assert llvm.predict(arr) == lgbm.predict(arr)
    arr = np.array([[1.0, 1.0, 1.0]], dtype=np.float64)
    assert llvm.predict(arr) == lgbm.predict(arr)
    arr = np.array([[0, 0, 0]], dtype=np.int32)
    assert llvm.predict(arr) == lgbm.predict(arr)
    arr = [[0, 0, 0]]
    assert llvm.predict(arr) == lgbm.predict(arr)