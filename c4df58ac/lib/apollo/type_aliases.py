import typing as _t

import altair as _al

import c4df58ac.lib.apollo.enums as _e

IntoDomain: _t.TypeAlias = _t.Union[str, _e.Domain]
Chart: _t.TypeAlias = _t.Union[_al.Chart, _al.LayerChart, _al.VConcatChart, _al.HConcatChart]
