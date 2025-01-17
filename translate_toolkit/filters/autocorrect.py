#
# Copyright 2005, 2006, 2009 Zuza Software Foundation
#
# This file is part of the Translate Toolkit.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

"""A set of autocorrect functions that fix common punctuation and space problems automatically"""

from translate_toolkit.filters import decoration


def correct(source, target):
    """Runs a set of easy and automatic corrections

    Current corrections include:
      - Ellipses - align target to use source form of ellipses (either three dots or the Unicode ellipses characters)
      - Missing whitespace and start or end of the target
      - Missing punction (.:?) at the end of the target
    """
    old_target = target
    if target == "":
        return None
    if "…" in source and "..." in target:
        target = target.replace("...", "…")
    elif "..." in source and "…" in target:
        target = target.replace("…", "...")
    if decoration.spacestart(source) != decoration.spacestart(
        target
    ) or decoration.spaceend(source) != decoration.spaceend(target):
        target = (
            decoration.spacestart(source) + target.strip() + decoration.spaceend(source)
        )
    punctuation = (".", ":", ". ", ": ", "?")
    puncendid = decoration.puncend(source, punctuation)
    puncendstr = decoration.puncend(target, punctuation)
    if puncendid != puncendstr:
        if not puncendstr:
            target = target + puncendid
        else:
            target = target[: -len(puncendstr)] + puncendid
    if source[:1].isalpha() and target[:1].isalpha():
        if source[:1].isupper() and target[:1].islower():
            target = target[:1].upper() + target[1:]
        elif source[:1].islower() and target[:1].isupper():
            target = target[:1].lower() + target[1:]
    if old_target != target:
        return target
    else:
        return None
