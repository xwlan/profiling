# -*- coding: utf-8 -*-
from __future__ import division
import sys

import pytest

from profiling.sampling import SamplingProfiler
from profiling.sampling.samplers import ItimerSampler
from utils import find_stats, spin


def spin_100ms():
    spin(0.1)


def spin_500ms():
    spin(0.5)


@pytest.mark.flaky(reruns=10)
def test_profiler():
    profiler = SamplingProfiler(top_frame=sys._getframe(),
                                sampler=ItimerSampler(0.0001))
    with profiler:
        spin_100ms()
        spin_500ms()
    stat1 = find_stats(profiler.stats, 'spin_100ms')
    stat2 = find_stats(profiler.stats, 'spin_500ms')
    ratio = stat1.deep_hits / stat2.deep_hits
    assert 0.8 <= ratio * 5 <= 1.2  # 1:5 expaected, but tolerate (0.8~1.2):5


def test_not_sampler():
    with pytest.raises(TypeError):
        SamplingProfiler(sampler=123)


def test_sample_1_depth():
    frame = sys._getframe()
    while frame.f_back is not None:
        frame = frame.f_back
    assert frame.f_back is None
    profiler = SamplingProfiler()
    profiler.sample(frame)
