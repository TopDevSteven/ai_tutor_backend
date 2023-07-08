from .. import list as lst


def test_flatMap():
    expected = [2, 4, 8, 3, 6, 9, 3, 5, 9]
    result = lst.flatMap(
        lambda x: map(lambda y: y + 1, x), [[1, 3, 7], [2, 5], [], [8, 2, 4, 8]]
    )
    assert list(result) == expected

    resultInnerEmpty = lst.flatMap(lambda x: map(lambda y: y + 1, x), [[], []])
    assert list(resultInnerEmpty) == []

    resultEmpty = lst.flatMap(lambda x: map(lambda y: y + 1, x), [])
    assert list(resultEmpty) == []
