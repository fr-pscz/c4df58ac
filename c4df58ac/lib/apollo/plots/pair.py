import typing as _t

import altair as _al
import polars as _pl
import polars.type_aliases as _pl_t

import c4df58ac.lib.apollo.axis as _ap_ax
import c4df58ac.lib.apollo.type_aliases as _ap_ta
import c4df58ac.lib.apollo.utils as _ap_u


def pair(  # pylint: disable=R0913
    data: _pl.DataFrame,
    features: _t.Sequence[_pl_t.IntoExprColumn],
    square_size: int = 100,
    **mark_args,
) -> _ap_ta.Chart:
    processed_data = data.select(*features)

    chart = None
    for feature_i in features:
        row_chart = None
        for feature_j in features:
            x_name = _ap_u.extract_name_from_intoexpr(feature_j)
            y_name = _ap_u.extract_name_from_intoexpr(feature_i)

            if x_name == y_name:
                _chart = (
                    _al.Chart(_pl.DataFrame({"text": [x_name]}))
                    .mark_text()
                    .encode(text="text:N")
                    .properties(width=square_size, height=square_size)
                )
            else:
                encoded_x = _al.X(
                    x_name + ":Q",
                    scale=_al.Scale(
                        domain=_ap_ax.AxisConfig("loose").get_domain(
                            processed_data.select(_pl.col(x_name)).to_series()
                        )
                    ),
                    title=None,
                    axis=_al.Axis(labels=False),
                )
                encoded_y = _al.Y(
                    y_name + ":Q",
                    scale=_al.Scale(
                        domain=_ap_ax.AxisConfig("loose").get_domain(
                            processed_data.select(_pl.col(y_name)).to_series()
                        )
                    ),
                    title=None,
                    axis=_al.Axis(labels=False),
                )

                _chart = (
                    _al.Chart(processed_data)
                    .mark_point(**mark_args)
                    .encode(
                        x=encoded_x,
                        y=encoded_y,
                    )
                    .properties(width=square_size, height=square_size)
                )
            if row_chart is None:
                row_chart = _chart
            else:
                row_chart = row_chart | _chart
        if chart is None:
            chart = row_chart
        else:
            chart = chart & row_chart

    if chart is None:
        raise ValueError("Not enough features.")

    return chart
