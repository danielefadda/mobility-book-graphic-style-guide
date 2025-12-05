import altair as alt
from builders.altair_builder import altair_from_tokens

@alt.theme.register("mobility_theme", enable=True)
def mobility_theme():
    return altair_from_tokens()
