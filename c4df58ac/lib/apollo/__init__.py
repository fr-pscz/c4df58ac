# import enum as _e
# import typing as _t

# import altair as _al
# import polars as _pl
# import polars.type_aliases as _pl_t
from altair import X, Y

import c4df58ac.lib.apollo.theme
from c4df58ac.lib.apollo.axis import AxisConfig
from c4df58ac.lib.apollo.enums import Domain
from c4df58ac.lib.apollo.plots import *

# def _iosevka():
#     font = "Iosevka Regular"

#     return {
#         "config": {
#             "title": {"font": font},
#             "axis": {"labelFont": font, "titleFont": font},
#             "header": {"labelFont": font, "titleFont": font},
#             "legend": {"labelFont": font, "titleFont": font},
#             "text": {"font": font},
#         }
#     }


# _al.themes.register("iosevka", _iosevka)
# _al.themes.enable("iosevka")


# class Domain(_e.Enum):
#     TIGHT = "tight"
#     ZERO_START = "zero_start"
#     LOOSE = "loose"


# IntoDomain: _t.TypeAlias = _t.Union[str, Domain]
# Chart: _t.TypeAlias = _t.Union[_al.Chart, _al.LayerChart, _al.VConcatChart, _al.HConcatChart]


# class AxisConfig:
#     def __init__(self, domain: IntoDomain = "loose"):
#         self.domain = Domain(domain)

#     def get_domain(self, series: _pl.Series, *more_series: _pl.Series) -> _t.List[float]:
#         domain = self.__get_domain_single(series)
#         for other_series in more_series:
#             new_domain = self.__get_domain_single(other_series)
#             domain[0] = min(domain[0], new_domain[0])
#             domain[1] = max(domain[1], new_domain[1])
#         return domain

#     def __get_domain_single(self, series: _pl.Series) -> _t.List[float]:
#         min_value = series.min()
#         max_value = series.max()

#         if not isinstance(min_value, _t.SupportsFloat) or not isinstance(
#             max_value, _t.SupportsFloat
#         ):
#             raise ValueError("Non numeric argument passed to numeric axis config.")

#         min_value = float(min_value)
#         max_value = float(max_value)

#         match self.domain:
#             case Domain.ZERO_START:
#                 if min_value * max_value < 0:
#                     raise ValueError("Series straddles 0, unclear where to place axis limits.")

#                 if min_value < 0:
#                     return [min_value * (1 + _LOOSE_AXIS_MARGIN), 0.0]
#                 return [0.0, max_value * (1 + _LOOSE_AXIS_MARGIN)]
#             case Domain.TIGHT:
#                 return [min_value, max_value]

#             case Domain.LOOSE:
#                 total_range = max_value - min_value
#                 return [
#                     min_value - total_range * _LOOSE_AXIS_MARGIN,
#                     max_value + total_range * _LOOSE_AXIS_MARGIN,
#                 ]
#         raise ValueError("Domain option not recognised.")


# def line(  # pylint: disable=R0913
#     data: _pl.DataFrame,
#     x: _pl_t.IntoExprColumn,
#     y: _t.Union[_pl_t.IntoExprColumn, _t.Tuple[_pl_t.IntoExprColumn, ...]],
#     x_axis_config: _t.Optional[AxisConfig] = None,
#     y_axis_config: _t.Optional[AxisConfig] = None,
#     legend_title: _t.Optional[str] = None,
#     y_label: _t.Optional[str] = None,
#     **mark_args,
# ) -> Chart:
#     if x_axis_config is None:
#         x_axis_config = AxisConfig(domain=Domain("tight"))
#     if y_axis_config is None:
#         y_axis_config = AxisConfig()

#     if not isinstance(y, tuple):
#         processed_data = data.select(x, y)
#     else:
#         processed_data = data.select(x, *y)

#     x_name = _extract_name_from_intoexpr(x)
#     encoded_x = _al.X(
#         x_name + ":Q",
#         scale=_al.Scale(
#             domain=x_axis_config.get_domain(processed_data.select(_pl.col(x_name)).to_series())
#         ),
#     )

#     if not isinstance(y, tuple):
#         y_name = _extract_name_from_intoexpr(y)
#         encoded_y = _al.Y(
#             y_name + ":Q",
#             scale=_al.Scale(
#                 domain=y_axis_config.get_domain(processed_data.select(_pl.col(y_name)).to_series())
#             ),
#         )
#         chart = (
#             _al.Chart(processed_data)
#             .mark_line(**mark_args)
#             .encode(
#                 x=encoded_x,
#                 y=encoded_y,
#             )
#         )
#     else:
#         ys = list(map(_extract_name_from_intoexpr, y))
#         y_name = y_label if y_label is not None else "value"
#         legend_title = legend_title if legend_title is not None else "variable"
#         encoded_y = _al.Y(
#             y_name + ":Q",
#             scale=_al.Scale(
#                 domain=y_axis_config.get_domain(
#                     *[processed_data.select(_pl.col(_)).to_series() for _ in ys]
#                 )
#             ),
#             **({"title": y_name} if y_label is not None else {}),
#         )
#         processed_data = processed_data.melt(
#             id_vars=x_name,
#             value_vars=ys,
#             value_name=y_name,
#             variable_name=legend_title,
#         )
#         chart = (
#             _al.Chart(processed_data)
#             .mark_line(**mark_args)
#             .encode(x=encoded_x, y=encoded_y, color=legend_title + ":N")
#         )

#     return chart


# def band(  # pylint: disable=R0913
#     data: _pl.DataFrame,
#     x: _pl_t.IntoExprColumn,
#     y_min: _pl_t.IntoExprColumn,
#     y_max: _pl_t.IntoExprColumn,
#     x_axis_config: _t.Optional[AxisConfig] = None,
#     y_axis_config: _t.Optional[AxisConfig] = None,
#     **mark_args,
# ) -> Chart:
#     if x_axis_config is None:
#         x_axis_config = AxisConfig(domain=Domain("tight"))
#     if y_axis_config is None:
#         y_axis_config = AxisConfig()

#     processed_data = data.select(x, y_min, y_max)

#     x_name = _extract_name_from_intoexpr(x)
#     y_min_name = _extract_name_from_intoexpr(y_min)
#     y_max_name = _extract_name_from_intoexpr(y_max)

#     chart = (
#         _al.Chart(processed_data)
#         .mark_area(**mark_args)
#         .encode(
#             x=_al.X(
#                 x_name + ":Q",
#                 scale=_al.Scale(
#                     domain=x_axis_config.get_domain(
#                         processed_data.select(_pl.col(x_name)).to_series()
#                     )
#                 ),
#             ),
#             y=_al.Y(
#                 y_min_name + ":Q",
#                 scale=_al.Scale(
#                     domain=y_axis_config.get_domain(
#                         processed_data.select(_pl.col(y_min_name)).to_series(),
#                         processed_data.select(_pl.col(y_max_name)).to_series(),
#                     )
#                 ),
#             ),
#             y2=y_max_name + ":Q",
#         )
#     )

#     if mark_args.get("opacity") is not None:

#         chart += (
#             _al.Chart(processed_data)
#             .mark_line(**mark_args)
#             .encode(
#                 x=x_name + ":Q",
#                 y=y_min_name + ":Q",
#             )
#         )
#         chart += (
#             _al.Chart(processed_data)
#             .mark_line(**mark_args)
#             .encode(
#                 x=x_name + ":Q",
#                 y=y_max_name + ":Q",
#             )
#         )

#     return chart


# def scatter(  # pylint: disable=R0913
#     data: _pl.DataFrame,
#     x: _pl_t.IntoExprColumn,
#     y: _pl_t.IntoExprColumn,
#     x_axis_config: _t.Optional[AxisConfig] = None,
#     y_axis_config: _t.Optional[AxisConfig] = None,
#     **mark_args,
# ) -> Chart:
#     if x_axis_config is None:
#         x_axis_config = AxisConfig(domain=Domain("loose"))
#     if y_axis_config is None:
#         y_axis_config = AxisConfig(domain=Domain("loose"))

#     processed_data = data.select(x, y)

#     x_name = _extract_name_from_intoexpr(x)
#     encoded_x = _al.X(
#         x_name + ":Q",
#         scale=_al.Scale(
#             domain=x_axis_config.get_domain(processed_data.select(_pl.col(x_name)).to_series())
#         ),
#     )

#     y_name = _extract_name_from_intoexpr(y)
#     encoded_y = _al.Y(
#         y_name + ":Q",
#         scale=_al.Scale(
#             domain=y_axis_config.get_domain(processed_data.select(_pl.col(y_name)).to_series())
#         ),
#     )
#     chart = (
#         _al.Chart(processed_data)
#         .mark_point(**mark_args)
#         .encode(
#             x=encoded_x,
#             y=encoded_y,
#         )
#     )

#     return chart


# def pair(  # pylint: disable=R0913
#     data: _pl.DataFrame,
#     features: _t.Sequence[_pl_t.IntoExprColumn],
#     square_size: int = 100,
#     **mark_args,
# ) -> Chart:
#     processed_data = data.select(*features)

#     chart = None
#     for feature_i in features:
#         row_chart = None
#         for feature_j in features:
#             x_name = _extract_name_from_intoexpr(feature_j)
#             y_name = _extract_name_from_intoexpr(feature_i)

#             if x_name == y_name:
#                 _chart = (
#                     _al.Chart(_pl.DataFrame({"text": [x_name]}))
#                     .mark_text()
#                     .encode(text="text:N")
#                     .properties(width=square_size, height=square_size)
#                 )
#             else:
#                 encoded_x = _al.X(
#                     x_name + ":Q",
#                     scale=_al.Scale(
#                         domain=AxisConfig("loose").get_domain(
#                             processed_data.select(_pl.col(x_name)).to_series()
#                         )
#                     ),
#                     title=None,
#                     axis=_al.Axis(labels=False),
#                 )
#                 encoded_y = _al.Y(
#                     y_name + ":Q",
#                     scale=_al.Scale(
#                         domain=AxisConfig("loose").get_domain(
#                             processed_data.select(_pl.col(y_name)).to_series()
#                         )
#                     ),
#                     title=None,
#                     axis=_al.Axis(labels=False),
#                 )

#                 _chart = (
#                     _al.Chart(processed_data)
#                     .mark_point(**mark_args)
#                     .encode(
#                         x=encoded_x,
#                         y=encoded_y,
#                     )
#                     .properties(width=square_size, height=square_size)
#                 )
#             if row_chart is None:
#                 row_chart = _chart
#             else:
#                 row_chart = row_chart | _chart
#         if chart is None:
#             chart = row_chart
#         else:
#             chart = chart & row_chart

#     if chart is None:
#         raise ValueError("Not enough features.")

#     return chart


# _LOOSE_AXIS_MARGIN = 0.1


# def _extract_name_from_intoexpr(x: _pl_t.IntoExprColumn):
#     if isinstance(x, _pl.Series):
#         return x.name
#     if isinstance(x, str):
#         return x
#     return x.meta.output_name()
