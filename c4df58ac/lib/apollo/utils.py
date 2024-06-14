import polars as _pl
import polars.type_aliases as _pl_t


def extract_name_from_intoexpr(x: _pl_t.IntoExprColumn):
    if isinstance(x, _pl.Series):
        return x.name
    if isinstance(x, str):
        return x
    return x.meta.output_name()
