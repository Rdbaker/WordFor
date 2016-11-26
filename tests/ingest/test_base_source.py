# -*- encoding: utf-8 -*-
"""Search models tests."""
import pytest

from wordfor.ingest.base_source import BaseSource


class TestBaseSource:
    def test_crawl_raises_error(self):
        source = BaseSource()
        with pytest.raises(NotImplementedError):
            source.crawl()

    def test_extract_raises_error(self):
        source = BaseSource()
        with pytest.raises(NotImplementedError):
            source.extract()
