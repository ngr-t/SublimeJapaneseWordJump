"""Jump based on tokens segmented by `tinysegmenter`.

Copyright (c) 2016, NEGORO Tetsuya (https://github.com/ngr-t)
This package is under new BSD License.

This package includes TinySegmenter.
http://pypi.python.org/pypi/tinysegmenter
Copyright (c) 2008, Taku Kudo
Copyright (c) 2010, Masato Hagiwara
Copyright (c) 2012, Jehan
TinySegmenter is released under new BSD License.
See `lib/tinysegmenter/COPYING` for details.

"""

import sublime
import sublime_plugin
from .lib.tinysegmenter import TinySegmenter

SEGMENTER = TinySegmenter()


def _get_next_word_end(text: str, cursor_pos: int) -> int:
    current = 0
    for token in SEGMENTER.tokenize(text):
        current += len(token)
        if cursor_pos < current:
            return current - cursor_pos
    return len(text) - cursor_pos


def _get_previous_word_end(text: str, cursor_pos: int) -> int:
    previous = 0
    current = 0
    for token in SEGMENTER.tokenize(text):
        current += len(token)
        if cursor_pos <= current:
            return previous - cursor_pos
        previous = current
    return len(text) - cursor_pos


class _TinySegmenterWordJumpCommand(sublime_plugin.TextCommand):
    """Jump based on tokens segmented by `tinysegmenter`."""

    def _get_tokenized_text_start_point(self, pos):
        view = self.view
        curr_row = view.rowcol(pos)[0]
        return max(0, view.text_point(curr_row - 1, 0))

    def _get_tokenized_text_end_point(self, pos):
        view = self.view
        curr_row = view.rowcol(pos)[0]
        return max(self.view.size(), view.text_point(curr_row + 2, -1))

    def _get_nearby_region(self, pos: int) -> str:
        region = sublime.Region(
            self._get_tokenized_text_start_point(pos),
            self._get_tokenized_text_end_point(pos))
        return self.view.substr(region)


class TinySegmenterWordJumpForward(_TinySegmenterWordJumpCommand):
    """Jump forward based on tokens segmented by `tinysegmenter`."""

    def run(self, edit):
        """Command definition."""
        view = self.view
        sel = view.sel()
        next_sel = [
            s.begin() + _get_next_word_end(
                self._get_nearby_region(s.begin()),
                s.begin() - self._get_tokenized_text_start_point(s.begin()))
            for s in sel]
        sel.clear()
        sel.add_all(sublime.Region(s, s) for s in next_sel)


class TinySegmenterWordJumpBack(_TinySegmenterWordJumpCommand):
    """Jump previous based on tokens segmented by `tinysegmenter`."""

    def run(self, edit):
        """Command definition."""
        view = self.view
        sel = view.sel()
        next_sel = [
            s.begin() + _get_previous_word_end(
                self._get_nearby_region(s.begin()),
                s.begin() - self._get_tokenized_text_start_point(s.begin()))
            for s in sel]
        print(next_sel)
        sel.clear()
        sel.add_all(sublime.Region(s, s) for s in next_sel)
