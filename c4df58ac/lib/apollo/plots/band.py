import typing as _t

import altair as _al
import polars as _pl
import polars.type_aliases as _pl_t

import c4df58ac.lib.apollo.axis as _ap_ax
import c4df58ac.lib.apollo.enums as _ap_e
import c4df58ac.lib.apollo.type_aliases as _ap_ta
import c4df58ac.lib.apollo.utils as _ap_u


def band(  # pylint: disable=R0913
    data: _pl.DataFrame,
    x: _pl_t.IntoExprColumn,
    y_min: _pl_t.IntoExprColumn,
    y_max: _pl_t.IntoExprColumn,
    x_axis_config: _t.Optional[_ap_ax.AxisConfig] = None,
    y_axis_config: _t.Optional[_ap_ax.AxisConfig] = None,
    **mark_args,
) -> _ap_ta.Chart:
    if x_axis_config is None:
        x_axis_config = _ap_ax.AxisConfig(domain=_ap_e.Domain("tight"))
    if y_axis_config is None:
        y_axis_config = _ap_ax.AxisConfig()

    processed_data = data.select(x, y_min, y_max)

    x_name = _ap_u.extract_name_from_intoexpr(x)
    y_min_name = _ap_u.extract_name_from_intoexpr(y_min)
    y_max_name = _ap_u.extract_name_from_intoexpr(y_max)

    chart = (
        _al.Chart(processed_data)
        .mark_area(**mark_args)
        .encode(
            x=_al.X(
                x_name + ":Q",
                scale=_al.Scale(
                    domain=x_axis_config.get_domain(
                        processed_data.select(_pl.col(x_name)).to_series()
                    )
                ),
            ),
            y=_al.Y(
                y_min_name + ":Q",
                scale=_al.Scale(
                    domain=y_axis_config.get_domain(
                        processed_data.select(_pl.col(y_min_name)).to_series(),
                        processed_data.select(_pl.col(y_max_name)).to_series(),
                    )
                ),
            ),
            y2=y_max_name + ":Q",
        )
    )

    if mark_args.get("opacity") is not None:

        chart += (
            _al.Chart(processed_data)
            .mark_line(**mark_args)
            .encode(
                x=x_name + ":Q",
                y=y_min_name + ":Q",
            )
        )
        chart += (
            _al.Chart(processed_data)
            .mark_line(**mark_args)
            .encode(
                x=x_name + ":Q",
                y=y_max_name + ":Q",
            )
        )

    return chart
