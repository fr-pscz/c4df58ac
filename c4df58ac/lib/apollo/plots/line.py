import typing as _t

import altair as _al
import polars as _pl
import polars.type_aliases as _pl_t

import c4df58ac.lib.apollo.axis as _ap_ax
import c4df58ac.lib.apollo.enums as _ap_e
import c4df58ac.lib.apollo.type_aliases as _ap_ta
import c4df58ac.lib.apollo.utils as _ap_u


def line(  # pylint: disable=R0913
    data: _pl.DataFrame,
    x: _pl_t.IntoExprColumn,
    y: _t.Union[_pl_t.IntoExprColumn, _t.Tuple[_pl_t.IntoExprColumn, ...]],
    x_axis_config: _t.Optional[_ap_ax.AxisConfig] = None,
    y_axis_config: _t.Optional[_ap_ax.AxisConfig] = None,
    legend_title: _t.Optional[str] = None,
    y_label: _t.Optional[str] = None,
    **mark_args,
) -> _ap_ta.Chart:
    if x_axis_config is None:
        x_axis_config = _ap_ax.AxisConfig(domain=_ap_e.Domain("tight"))
    if y_axis_config is None:
        y_axis_config = _ap_ax.AxisConfig()

    if not isinstance(y, tuple):
        processed_data = data.select(x, y)
    else:
        processed_data = data.select(x, *y)

    x_name = _ap_u.extract_name_from_intoexpr(x)
    encoded_x = _al.X(
        x_name + ":Q",
        scale=_al.Scale(
            domain=x_axis_config.get_domain(processed_data.select(_pl.col(x_name)).to_series())
        ),
    )

    if not isinstance(y, tuple):
        y_name = _ap_u.extract_name_from_intoexpr(y)
        encoded_y = _al.Y(
            y_name + ":Q",
            scale=_al.Scale(
                domain=y_axis_config.get_domain(processed_data.select(_pl.col(y_name)).to_series())
            ),
        )
        chart = (
            _al.Chart(processed_data)
            .mark_line(**mark_args)
            .encode(
                x=encoded_x,
                y=encoded_y,
            )
        )
    else:
        ys = list(map(_ap_u.extract_name_from_intoexpr, y))
        y_name = y_label if y_label is not None else "value"
        legend_title = legend_title if legend_title is not None else "variable"
        encoded_y = _al.Y(
            y_name + ":Q",
            scale=_al.Scale(
                domain=y_axis_config.get_domain(
                    *[processed_data.select(_pl.col(_)).to_series() for _ in ys]
                )
            ),
            **({"title": y_name} if y_label is not None else {}),
        )
        processed_data = processed_data.melt(
            id_vars=x_name,
            value_vars=ys,
            value_name=y_name,
            variable_name=legend_title,
        )
        chart = (
            _al.Chart(processed_data)
            .mark_line(**mark_args)
            .encode(x=encoded_x, y=encoded_y, color=legend_title + ":N")
        )

    return chart
