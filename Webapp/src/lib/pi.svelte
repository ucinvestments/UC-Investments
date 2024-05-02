<script>
  import { onMount, createEventDispatcher, afterUpdate } from "svelte";
  import * as d3 from "d3";

  export let filteredData;
  export let selectedSlice;
  export let activeButton;
  let width = 350;
  let height = 400;
  let radius = Math.min(width, height) / 2;
  let svg;
  let g;
  let color;
  let pie;
  let arcPath;
  let arcLabel;
  const dispatch = createEventDispatcher();

  function getRandomColor() {
    return `rgb(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)})`;
  }

  function cap(string) {
    return string
      .split(" ")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  }

  function drawChart() {
    if (!g) return;

    const validData = filteredData.length > 0 ? filteredData : [];

    const update = g.selectAll(".arc").data(pie(validData));

    const exit = update.exit().transition().duration(500).remove();

    exit.select("path").attrTween("d", function (d) {
      const interpolate = d3.interpolate(d, {
        startAngle: d.endAngle,
        endAngle: d.endAngle,
      });
      return function (t) {
        return arcPath(interpolate(t));
      };
    });

    exit.select("text").style("opacity", 0);

    const enter = update.enter().append("g").attr("class", "arc");
    const arcs = enter.merge(update);

    enter.append("path").on("click", handleSliceClick);

    if (activeButton == "Company") {
      arcs
        .select("path")
        .transition()
        .duration(500)
        .attrTween("d", function (d) {
          const interpolate = d3.interpolate(this._current, d);
          this._current = interpolate(0);
          return function (t) {
            return arcPath(interpolate(t));
          };
        })
        .attr("fill", (d) => getRandomColor())
        .attr("stroke", (d) => (d.data === selectedSlice ? "white" : "none"))
        .attr("stroke-width", (d) =>
          d.data === selectedSlice ? "2px" : "0px",
        );

      arcs
        .select("text")
        .transition()
        .duration(100)
        .attr("transform", (d) => `translate(${arcLabel.centroid(d)})`)
        .text((d) => (d.data === selectedSlice ? cap(d.data["asset"]) : ""))
        .style("opacity", 1);
    } else if (activeButton == "Fund") {
      arcs
        .select("path")
        .transition()
        .duration(500)
        .attrTween("d", function (d) {
          const interpolate = d3.interpolate(this._current, d);
          this._current = interpolate(0);
          return function (t) {
            return arcPath(interpolate(t));
          };
        })
        .attr("fill", (d) => getRandomColor())
        .attr("stroke", (d) => (d.data === selectedSlice ? "white" : "none"))
        .attr("stroke-width", (d) =>
          d.data === selectedSlice ? "2px" : "0px",
        );

      arcs
        .select("text")
        .transition()
        .duration(100)
        .attr("transform", (d) => `translate(${arcLabel.centroid(d)})`)
        .text((d) =>
          d.data === selectedSlice ? cap(d.data["Asset Name"]) : "",
        )
        .style("opacity", 1);
    } else {
      arcs
        .select("path")
        .transition()
        .duration(500)
        .attrTween("d", function (d) {
          const interpolate = d3.interpolate(this._current, d);
          this._current = interpolate(0);
          return function (t) {
            return arcPath(interpolate(t));
          };
        })
        .attr("fill", (d) => getRandomColor())
        .attr("stroke", (d) => (d.data === selectedSlice ? "white" : "none"))
        .attr("stroke-width", (d) =>
          d.data === selectedSlice ? "2px" : "0px",
        );

      arcs
        .select("text")
        .transition()
        .duration(100)
        .attr("transform", (d) => `translate(${arcLabel.centroid(d)})`)
        .text((d) =>
          d.data === selectedSlice ? cap(d.data["Asset Name"]) : "",
        )
        .style("opacity", 1);
      pie = d3.pie().value((d) => d["total_investment"]);
    }
    enter
      .append("text")
      .style("font-size", "12px")
      .style("fill", "var(--black)")
      .style("text-anchor", "middle")
      .style("opacity", 0)
      .transition()
      .duration(100)
      .style("opacity", 1);

    update.raise();
  }

  onMount(() => {
    color = d3.scaleOrdinal([
      "var(--sec)",
      "var(--founder)",
      "var(--medalist)",
      "var(--wellman)",
      "var(--bay-fog)",
      "var(--sather-gate)",
      "var(--rose-garden)",
      "var(--lawrence)",
      "var(--ion)",
      "var(--golden-gate)",
      "var(--lap-lane)",
      "var(--soybean)",
      "var(--south-hall)",
      "var(--pacific)",
      "var(--stone-pine)",
    ]);
    if (activeButton == "Company") {
      pie = d3.pie().value((d) => d["total investment"]);
    } else if (activeButton == "Fund") {
      pie = d3.pie().value((d) => d["Total Investment"]);
    } else {
      pie = d3.pie().value((d) => d["Total Iℂnvest∈d"]);
    }
    arcPath = d3
      .arc()
      .outerRadius(radius - 10)
      .innerRadius(0);
    arcLabel = d3
      .arc()
      .outerRadius(radius - 60)
      .innerRadius(radius - 60);

    svg = d3
      .select(".pie-chart")
      .append("svg")
      .attr("width", width)
      .attr("height", height);

    g = svg
      .append("g")
      .attr("transform", `translate(${width / 2}, ${height / 2})`);

    drawChart();
  });

  afterUpdate(drawChart);

  function handleSliceClick(event, data) {
    dispatch("sliceClicked", data.data);
  }
</script>

<div class="pie-chart m-auto" />

<style>
</style>
