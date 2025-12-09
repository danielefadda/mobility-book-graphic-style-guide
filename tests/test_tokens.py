"""Test sul loader dei design token."""

import mobility_book_style as mbs


def test_token_object_exposed():
    assert hasattr(mbs, "token")


def test_dot_notation_access():
    color = mbs.token.color.brand.primary
    assert isinstance(color, str)
    assert color.startswith("#")


def test_reference_resolution():
    # background.default punta a base.neutral.white nel JSON
    assert mbs.token.color.background.default.lower() == "#ffffff"


def test_token_dict_mirrors_object():
    from mobility_book_style._tokens import token_dict

    assert token_dict["color"]["brand"]["primary"] == mbs.token.color.brand.primary
    assert token_dict["font"]["family"]["sans"] == mbs.token.font.family.sans
