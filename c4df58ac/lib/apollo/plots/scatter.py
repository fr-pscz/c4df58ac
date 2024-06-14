import typing as _t

import altair as _al
import polars as _pl
import polars.type_aliases as _pl_t

import c4df58ac.lib.apollo.axis as _ap_ax
import c4df58ac.lib.apollo.enums as _ap_e
import c4df58ac.lib.apollo.type_aliases as _ap_ta
import c4df58ac.lib.apollo.utils as _ap_u


def scatter(  # pylint: disable=R0913
    data: _pl.DataFrame,
    x: _pl_t.IntoExprColumn,
    y: _pl_t.IntoExprColumn,
    x_axis_config: _t.Optional[_ap_ax.AxisConfig] = None,
    y_axis_config: _t.Optional[_ap_ax.AxisConfig] = None,
    **mark_args,
) -> _ap_ta.Chart:
    if x_axis_config is None:
        x_axis_config = _ap_ax.AxisConfig(domain=_ap_e.Domain("loose"))
    if y_axis_config is None:
        y_axis_config = _ap_ax.AxisConfig(domain=_ap_e.Domain("loose"))

    processed_data = data.select(x, y)

    x_name = _ap_u.extract_name_from_intoexpr(x)
    encoded_x = _al.X(
        x_name + ":Q",
        scale=_al.Scale(
            domain=x_axis_config.get_domain(processed_data.select(_pl.col(x_name)).to_series())
        ),
    )

    y_name = _ap_u.extract_name_from_intoexpr(y)
    encoded_y = _al.Y(
        y_name + ":Q",
        scale=_al.Scale(
            domain=y_axis_config.get_domain(processed_data.select(_pl.col(y_name)).to_series())
        ),
    )
    chart = (
        _al.Chart(processed_data)
        .mark_point(**mark_args)
        .encode(
            x=encoded_x,
            y=encoded_y,
        )
    )

    return chart
