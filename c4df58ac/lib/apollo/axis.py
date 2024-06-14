import typing as _t

import polars as _pl

import c4df58ac.lib.apollo.enums as _e
import c4df58ac.lib.apollo.type_aliases as _ta


class AxisConfig:
    def __init__(self, domain: _ta.IntoDomain = "loose"):
        self.domain = _e.Domain(domain)

    def get_domain(self, series: _pl.Series, *more_series: _pl.Series) -> _t.List[float]:
        domain = self.__get_domain_single(series)
        for other_series in more_series:
            new_domain = self.__get_domain_single(other_series)
            domain[0] = min(domain[0], new_domain[0])
            domain[1] = max(domain[1], new_domain[1])
        return domain

    def __get_domain_single(self, series: _pl.Series) -> _t.List[float]:
        min_value = series.min()
        max_value = series.max()

        if not isinstance(min_value, _t.SupportsFloat) or not isinstance(
            max_value, _t.SupportsFloat
        ):
            raise ValueError("Non numeric argument passed to numeric axis config.")

        min_value = float(min_value)
        max_value = float(max_value)

        match self.domain:
            case _e.Domain.ZERO_START:
                if min_value * max_value < 0:
                    raise ValueError("Series straddles 0, unclear where to place axis limits.")

                if min_value < 0:
                    return [min_value * (1 + _LOOSE_AXIS_MARGIN), 0.0]
                return [0.0, max_value * (1 + _LOOSE_AXIS_MARGIN)]
            case _e.Domain.TIGHT:
                return [min_value, max_value]

            case _e.Domain.LOOSE:
                total_range = max_value - min_value
                return [
                    min_value - total_range * _LOOSE_AXIS_MARGIN,
                    max_value + total_range * _LOOSE_AXIS_MARGIN,
                ]
        raise ValueError("Domain option not recognised.")


_LOOSE_AXIS_MARGIN = 0.1
