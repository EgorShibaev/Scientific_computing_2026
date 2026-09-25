#!/usr/bin/env python3
"""Polish native, editable PowerPoint chart axes, lines, and markers.

Usage:
    python3 set-chart-log-axes.py INPUT.pptx OUTPUT.pptx PLAN.json

PLAN.json is an array, for example:
    [{"chartIndex": 2, "xLog": true, "yLog": false},
     {"chartIndex": 7, "xLog": true, "yLog": true}]

chartIndex selects chartN.xml in ppt/charts/ or ppt/slides/charts/, not a
chart's order on a slide. Ambiguous indices present in both locations fail.
True flags enable base-10 scaling; false or absent flags leave an axis alone.
Optional axesAtMin moves both value axes to the minimum. straightLines disables
curve smoothing. markerStyles can contain objects such as
{"seriesIndex": 2, "color": "C46A13", "size": 8}; seriesIndex is one-based.
Only selected chart XML is changed. All other ZIP-member payloads, including
embedded workbooks, are preserved byte-for-byte. Input and output may coincide.
The input chart must use a numeric value axis for each requested log axis.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import tempfile
from xml.dom import Node, minidom
from zipfile import BadZipFile, ZipFile


class ChartError(ValueError):
    """The requested edit cannot safely be applied to a chart."""


def child_elements(parent, name, namespace):
    return [
        node for node in parent.childNodes
        if node.nodeType == Node.ELEMENT_NODE
        and node.namespaceURI == namespace
        and node.localName == name
    ]


def one_child(parent, name, namespace, *, required=True):
    children = child_elements(parent, name, namespace)
    if len(children) > 1:
        raise ChartError(f"Multiple {name} elements in {parent.nodeName}")
    if not children:
        if required:
            raise ChartError(f"Missing {name} in {parent.nodeName}")
        return None
    return children[0]


def make_element(document, reference, name):
    prefix = f"{reference.prefix}:" if reference.prefix else ""
    return document.createElementNS(reference.namespaceURI, prefix + name)


def remove_children(parent, names, namespace):
    for name in names:
        for node in child_elements(parent, name, namespace):
            parent.removeChild(node)
            node.unlink()


def enable_log_axis(document, axis, namespace):
    scaling = one_child(axis, "scaling", namespace)
    for bound_name in ("min", "max"):
        bound = one_child(scaling, bound_name, namespace, required=False)
        if bound is None:
            continue
        raw = bound.getAttribute("val")
        try:
            value = float(raw)
        except ValueError as exc:
            raise ChartError(f"Invalid {bound_name} value: {raw!r}") from exc
        if not math.isfinite(value) or value <= 0:
            raise ChartError(
                f"Logarithmic axes require positive finite bounds; "
                f"{bound_name}={raw!r}"
            )
    log_base = one_child(scaling, "logBase", namespace, required=False)
    if log_base is None:
        log_base = make_element(document, scaling, "logBase")
        # CT_Scaling puts logBase before orientation, max, min, and extLst.
        scaling.insertBefore(log_base, scaling.firstChild)
    log_base.setAttribute("val", "10")
    remove_children(axis, ("majorUnit", "minorUnit"), namespace)


def cross_at_minimum(document, axis, namespace):
    remove_children(axis, ("crosses", "crossesAt"), namespace)
    cross_axis = one_child(axis, "crossAx", namespace)
    crossing = make_element(document, axis, "crosses")
    crossing.setAttribute("val", "min")
    # In all chart axis types, crosses/crossesAt follows crossAx.
    axis.insertBefore(crossing, cross_axis.nextSibling)


def nearest_plot_area(axis, namespace):
    parent = axis.parentNode
    while parent is not None:
        if (parent.nodeType == Node.ELEMENT_NODE
                and parent.namespaceURI == namespace
                and parent.localName == "plotArea"):
            return parent
        parent = parent.parentNode
    raise ChartError("Value axis is not inside a plotArea")


def insert_before_first(parent, element, names, namespace):
    for child in parent.childNodes:
        if (child.nodeType == Node.ELEMENT_NODE
                and child.namespaceURI == namespace
                and child.localName in names):
            parent.insertBefore(element, child)
            return
    parent.appendChild(element)


def disable_smoothing(document, series, namespace):
    if series.parentNode.localName not in ("scatterChart", "lineChart", "line3DChart"):
        raise ChartError("straightLines requires scatter or line chart series")
    smooth = one_child(series, "smooth", namespace, required=False)
    if smooth is None:
        smooth = make_element(document, series, "smooth")
        insert_before_first(series, smooth, {"extLst"}, namespace)
    smooth.setAttribute("val", "0")


def style_marker(document, series, style, namespace):
    if series.parentNode.localName not in ("scatterChart", "lineChart", "line3DChart"):
        raise ChartError("markerStyles requires scatter or line chart series")
    marker = one_child(series, "marker", namespace, required=False)
    if marker is None:
        marker = make_element(document, series, "marker")
        insert_before_first(
            series, marker,
            {"dPt", "dLbls", "trendline", "errBars", "cat", "val",
             "xVal", "yVal", "smooth", "extLst"}, namespace,
        )
    remove_children(marker, ("symbol", "size", "spPr"), namespace)
    symbol = make_element(document, marker, "symbol")
    symbol.setAttribute("val", "circle")
    size = make_element(document, marker, "size")
    size.setAttribute("val", str(style["size"]))
    properties = make_element(document, marker, "spPr")
    drawing_namespace = (
        "http://purl.oclc.org/ooxml/drawingml/main"
        if namespace == "http://purl.oclc.org/ooxml/drawingml/chart"
        else "http://schemas.openxmlformats.org/drawingml/2006/main"
    )
    # A local declaration is valid even when the input declares DrawingML
    # prefixes only on individual descendant elements (as some exporters do).
    properties.setAttributeNS(
        "http://www.w3.org/2000/xmlns/", "xmlns:a", drawing_namespace,
    )

    def solid_fill():
        fill = document.createElementNS(drawing_namespace, "a:solidFill")
        color = document.createElementNS(drawing_namespace, "a:srgbClr")
        color.setAttribute("val", style["color"].upper())
        fill.appendChild(color)
        return fill

    properties.appendChild(solid_fill())
    outline = document.createElementNS(drawing_namespace, "a:ln")
    outline.setAttribute("w", "19050")
    outline.appendChild(solid_fill())
    properties.appendChild(outline)
    for element in (symbol, size, properties):
        insert_before_first(marker, element, {"extLst"}, namespace)
    if series.parentNode.localName == "scatterChart":
        scatter = series.parentNode
        scatter_style = one_child(scatter, "scatterStyle", namespace, required=False)
        if scatter_style is None:
            scatter_style = make_element(document, scatter, "scatterStyle")
            scatter.insertBefore(scatter_style, scatter.firstChild)
        scatter_style.setAttribute("val", "lineMarker")


def patch_chart(xml_bytes, plan):
    document = minidom.parseString(xml_bytes)
    try:
        namespace = document.documentElement.namespaceURI
        if not namespace or document.documentElement.localName != "chartSpace":
            raise ChartError("Expected a namespaced chartSpace document")
        axes = list(document.getElementsByTagNameNS(namespace, "valAx"))
        requested = []
        for direction, positions in (("x", {"b", "t"}), ("y", {"l", "r"})):
            if not plan.get(direction + "Log", False):
                continue
            matches = [
                axis for axis in axes
                if one_child(axis, "axPos", namespace).getAttribute("val")
                in positions
            ]
            if not matches:
                raise ChartError(f"No numeric {direction}-axis found")
            requested.extend(matches)

        for axis in requested:
            enable_log_axis(document, axis, namespace)
            cross_id = one_child(axis, "crossAx", namespace).getAttribute("val")
            plot_area = nearest_plot_area(axis, namespace)
            partners = []
            for axis_type in ("valAx", "catAx", "dateAx", "serAx"):
                for candidate in child_elements(plot_area, axis_type, namespace):
                    candidate_id = one_child(candidate, "axId", namespace)
                    if candidate_id.getAttribute("val") == cross_id:
                        partners.append(candidate)
            if len(partners) != 1:
                raise ChartError(
                    f"Expected one perpendicular axis with axId={cross_id!r}; "
                    f"found {len(partners)}"
                )
            # The partner's crossing setting controls its position on this
            # logarithmic axis. Zero is outside the positive log domain.
            cross_at_minimum(document, partners[0], namespace)
        if plan.get("axesAtMin"):
            for axis in axes:
                cross_at_minimum(document, axis, namespace)
        series = list(document.getElementsByTagNameNS(namespace, "ser"))
        if plan.get("straightLines"):
            for item in series:
                disable_smoothing(document, item, namespace)
        for style in plan.get("markerStyles", []):
            index = style["seriesIndex"]
            if index > len(series):
                raise ChartError(f"seriesIndex {index} exceeds {len(series)} series")
            style_marker(document, series[index - 1], style, namespace)
        return document.toxml(encoding="UTF-8")
    finally:
        document.unlink()


def read_plan(path):
    with path.open(encoding="utf-8") as handle:
        plan = json.load(handle)
    if not isinstance(plan, list):
        raise ChartError("Plan must be a JSON array")
    selected = {}
    for entry in plan:
        if not isinstance(entry, dict):
            raise ChartError("Every plan entry must be an object")
        extra = set(entry) - {
            "chartIndex", "xLog", "yLog", "axesAtMin", "straightLines", "markerStyles",
        }
        if extra:
            raise ChartError(f"Unknown plan fields: {', '.join(sorted(extra))}")
        index = entry.get("chartIndex")
        if type(index) is not int or index < 1:
            raise ChartError("chartIndex must be a positive integer")
        for flag in ("xLog", "yLog", "axesAtMin", "straightLines"):
            if flag in entry and type(entry[flag]) is not bool:
                raise ChartError(f"{flag} must be true or false")
        styles = entry.get("markerStyles", [])
        if not isinstance(styles, list):
            raise ChartError("markerStyles must be an array")
        styled_indices = set()
        for style in styles:
            if not isinstance(style, dict) or set(style) != {"seriesIndex", "color", "size"}:
                raise ChartError("Each marker style requires seriesIndex, color, and size")
            series_index = style["seriesIndex"]
            if type(series_index) is not int or series_index < 1:
                raise ChartError("seriesIndex must be a positive integer")
            if series_index in styled_indices:
                raise ChartError(f"Duplicate marker seriesIndex: {series_index}")
            styled_indices.add(series_index)
            if type(style["size"]) is not int or not 2 <= style["size"] <= 72:
                raise ChartError("Marker size must be an integer between 2 and 72")
            if not isinstance(style["color"], str) or not re.fullmatch(r"[0-9a-fA-F]{6}", style["color"]):
                raise ChartError("Marker color must contain exactly six hexadecimal digits")
        if index in selected:
            raise ChartError(f"Duplicate chartIndex: {index}")
        selected[index] = entry
    return selected


def patch_presentation(input_path, output_path, plan_path):
    plan = read_plan(plan_path)
    patched = {}
    with ZipFile(input_path, "r") as source:
        members = source.namelist()
        for index, entry in plan.items():
            candidates = (
                f"ppt/charts/chart{index}.xml",
                f"ppt/slides/charts/chart{index}.xml",
            )
            matches = [member for member in members if member in candidates]
            if len(matches) != 1:
                raise ChartError(
                    f"Expected exactly one chart{index}.xml in ppt/charts/ "
                    f"or ppt/slides/charts/; found {len(matches)}"
                )
            member = matches[0]
            if any(entry.get(key) for key in (
                "xLog", "yLog", "axesAtMin", "straightLines", "markerStyles",
            )):
                try:
                    patched[member] = patch_chart(source.read(member), entry)
                except Exception as exc:
                    raise ChartError(f"{member}: {exc}") from exc

        # Validate and patch before creating output. An atomic rename keeps
        # existing decks safe even for in-place use or an interrupted write.
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                prefix=f".{output_path.name}.", suffix=".tmp",
                dir=output_path.parent, delete=False,
            ) as handle:
                temporary = Path(handle.name)
            with ZipFile(temporary, "w") as destination:
                destination.comment = source.comment
                for info in source.infolist():
                    payload = (patched[info.filename] if info.filename in patched
                               else source.read(info))
                    destination.writestr(info, payload)
            os.replace(temporary, output_path)
            temporary = None
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    return len(patched)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", type=Path, help="Input PPTX")
    parser.add_argument("output", type=Path, help="Output PPTX (may equal input)")
    parser.add_argument("plan", type=Path, help="JSON array of chart-axis edits")
    args = parser.parse_args()
    try:
        count = patch_presentation(args.input, args.output, args.plan)
    except (ChartError, OSError, ValueError, BadZipFile) as exc:
        parser.exit(1, f"error: {exc}\n")
    print(f"Updated {count} native chart(s): {args.output}")


if __name__ == "__main__":
    main()
