#
# Copyright 2008-2009 Zuza Software Foundation
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

"""
Contains the ``parse`` function that parses normal strings into StringElem-
based "rich" string element trees.
"""


from translate_toolkit.storage.placeables.strelem import StringElem


def parse(tree, parse_funcs):
    """Parse placeables from the given string or sub-tree by using the
    parsing functions provided.

    The output of this function is **heavily** dependent on the order of the
    parsing functions. This is because of the algorithm used.

    An over-simplification of the algorithm: the leaves in the ``StringElem``
    tree are expanded to the output of the first parsing function in
    ``parse_funcs``. The next level of recursion is then started on the new
    set of leaves with the used parsing function removed from
    ``parse_funcs``.

    :type  tree: unicode|StringElem
    :param tree: The string or string element sub-tree to parse.
    :type  parse_funcs: A list of parsing functions. It must take exactly
                        one argument (a ``unicode`` string to parse) and
                        return a list of ``StringElem``s which, together,
                        form the original string. If nothing could be
                        parsed, it should return ``None``.
    """
    if isinstance(tree, str):
        tree = StringElem(tree)
    if not parse_funcs:
        return tree

    parse_func = parse_funcs[0]

    for leaf in tree.flatten():
        # FIXME: we might rather want to test for editability, but for now this
        # works better
        if not leaf.istranslatable:
            continue

        unileaf = str(leaf)
        if not unileaf:
            continue

        subleaves = parse_func(unileaf)
        if subleaves is not None:
            if (
                len(subleaves) == 1
                and isinstance(subleaves[0], type(leaf))
                and leaf == subleaves[0]
            ):
                pass
            elif isinstance(leaf, str):
                parent = tree.get_parent_elem(leaf)
                if parent is not None:
                    if len(parent.sub) == 1:
                        parent.sub = subleaves
                        leaf = parent
                    else:
                        leafindex = parent.sub.index(leaf)
                        parent.sub[leafindex] = StringElem(subleaves)
                        leaf = parent.sub[leafindex]
            else:
                leaf.sub = subleaves

        parse(leaf, parse_funcs[1:])

        if isinstance(leaf, StringElem):
            leaf.prune()
    return tree
