<script>
  import { onMount, createEventDispatcher, afterUpdate } from "svelte";
  import * as d3 from "d3";

  export let filteredData;
  export let selectedSlice;
  export let activeButton;
  export let totalInvestedInChart;
  
  let width = 380;
  let height = 380;
  let radius = Math.min(width, height) / 2;
  let svg;
  let g;
  let tooltip;
  let pie;
  let arcPath;
  let arcHover;
  const dispatch = createEventDispatcher();
  
  const MAX_ITEMS = 25; // Maximum items to show before aggregating

  const colorPalette = [
    "#3B7EA1", "#FDB515", "#003262", "#C4820E", "#00B0DA", 
    "#00A598", "#859438", "#ED4E33", "#D9661F", "#EE1F60", 
    "#46535E", "#6C3302", "#CFDD45", "#B9D3B6", "#DDD5C7",
    // Additional colors for more variety
    "#8B4513", "#2E8B57", "#4682B4", "#CD853F", "#FF6347",
    "#4169E1", "#32CD32", "#FFD700", "#FF69B4", "#8A2BE2"
  ];

  function getColor(index) {
    return colorPalette[index % colorPalette.length];
  }

  function cap(string) {
    if (!string) return "";
    return string
      .split(" ")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  }

  function formatValue(value) {
    if (value >= 1e9) return `$${(value / 1e9).toFixed(1)}B`;
    if (value >= 1e6) return `$${(value / 1e6).toFixed(1)}M`;
    if (value >= 1e3) return `$${(value / 1e3).toFixed(1)}K`;
    return `$${value}`;
  }

  function processDataForChart(data) {
    if (!data || data.length === 0) return [];

    // Sort data by value (descending) - handle different value fields
    const sortedData = [...data].sort((a, b) => {
      let valueA = 0, valueB = 0;
      
      if (activeButton == "Company") {
        valueA = Number(a["total investment"]) || 0;
        valueB = Number(b["total investment"]) || 0;
      } else if (activeButton == "Fund") {
        valueA = Number(a["Total Investment"]) || 0;
        valueB = Number(b["Total Investment"]) || 0;
      } else {
        valueA = Number(a["Total Iℂnvest∈d"]) || 0;
        valueB = Number(b["Total Iℂnvest∈d"]) || 0;
      }
      
      return valueB - valueA;
    });

    console.log(`Processing ${sortedData.length} items for ${activeButton}, MAX_ITEMS: ${MAX_ITEMS}`);

    // If we have more than MAX_ITEMS, aggregate the rest
    if (sortedData.length <= MAX_ITEMS) {
      console.log(`Returning all ${sortedData.length} items (under limit)`);
      return sortedData;
    }

    const topItems = sortedData.slice(0, MAX_ITEMS - 1);
    const remainingItems = sortedData.slice(MAX_ITEMS - 1);
    
    console.log(`Limiting to ${topItems.length} items, aggregating ${remainingItems.length} others`);
    
    // Calculate aggregate value for remaining items
    let aggregateValue = 0;
    remainingItems.forEach(item => {
      let itemValue = 0;
      if (activeButton == "Company") {
        itemValue = Number(item["total investment"]) || 0;
      } else if (activeButton == "Fund") {
        itemValue = Number(item["Total Investment"]) || 0;
      } else {
        itemValue = Number(item["Total Iℂnvest∈d"]) || 0;
      }
      aggregateValue += itemValue;
    });

    // Create "Others" item
    const othersItem = {
      isAggregate: true,
      aggregatedCount: remainingItems.length,
      aggregatedItems: remainingItems
    };

    if (activeButton == "Company") {
      othersItem["asset"] = `Others (${remainingItems.length} companies)`;
      othersItem["total investment"] = aggregateValue;
      othersItem["funding sources"] = [];
    } else if (activeButton == "Fund") {
      othersItem["Asset Name"] = `Others (${remainingItems.length} funds)`;
      othersItem["Total Investment"] = aggregateValue;
      othersItem["Asset Type"] = "Aggregated";
      othersItem["Funding Sources"] = [];
    } else {
      othersItem["A.s.set ._Class"] = `Others (${remainingItems.length} asset classes)`;
      othersItem["Total Iℂnvest∈d"] = aggregateValue;
      othersItem["InVesTmeNts"] = [`${remainingItems.length} aggregated asset classes`];
    }

    console.log(`Created Others item with value: ${aggregateValue}`);
    return [...topItems, othersItem];
  }

  function drawChart() {
    if (!g) return;
    
    // Handle null or undefined data
    if (!filteredData || !Array.isArray(filteredData)) {
      console.log('No valid data available for chart:', filteredData);
      // Clear chart if no data
      g.selectAll(".arc").remove();
      g.selectAll(".center-text").remove();
      return;
    }

    console.log(`Drawing chart for ${activeButton} with ${filteredData.length} raw items`);
    const processedData = processDataForChart(filteredData);
    console.log(`Processed data has ${processedData.length} items for chart`);
    
    // Clear previous chart
    g.selectAll(".arc").remove();
    g.selectAll(".center-text").remove();

    if (processedData.length === 0) {
      console.log('No processed data available for chart');
      return;
    }

    // Create pie data
    const pieData = pie(processedData);
    console.log(`Created ${pieData.length} pie slices`);

    // Create arcs
    const arcs = g.selectAll(".arc")
      .data(pieData)
      .enter()
      .append("g")
      .attr("class", "arc")
      .style("cursor", "pointer");
    
    console.log(`Created ${arcs.size()} arc elements`);

    // Add paths with animation
    arcs.append("path")
      .attr("class", "arc-path")
      .attr("fill", (d, i) => {
        // Use a slightly different color for "Others" item
        if (d.data.isAggregate) {
          return "#8B8B8B"; // Gray color for aggregated items
        }
        return getColor(i);
      })
      .attr("stroke", (d) => d.data === selectedSlice ? "white" : "none")
      .attr("stroke-width", (d) => d.data === selectedSlice ? "3px" : "0px")
      .style("filter", (d) => d.data === selectedSlice ? "brightness(1.1)" : "none")
      .on("click", handleSliceClick)
      .on("mouseenter", handleMouseEnter)
      .on("mouseleave", handleMouseLeave)
      .transition()
      .duration(750)
      .attrTween("d", function(d) {
        const interpolate = d3.interpolate({ startAngle: 0, endAngle: 0 }, d);
        return function(t) {
          return arcPath(interpolate(t));
        };
      });

    // Update center label
    updateCenterLabel();
  }

  function updateCenterLabel() {
    if (!g || !selectedSlice) return;

    // Remove existing center text
    g.selectAll(".center-text").remove();

    const centerGroup = g.append("g")
      .attr("class", "center-text")
      .style("opacity", 0);

    // Get data based on active button
    let name = "";
    let value = 0;
    let percentage = 0;

    if (selectedSlice.isAggregate) {
      // Handle aggregated item
      name = selectedSlice.aggregatedCount + " Others";
      if (activeButton == "Company") {
        value = selectedSlice["total investment"];
      } else if (activeButton == "Fund") {
        value = selectedSlice["Total Investment"];
      } else {
        value = selectedSlice["Total Iℂnvest∈d"];
      }
    } else {
      // Handle regular item
      if (activeButton == "Company") {
        name = cap(selectedSlice["asset"]);
        value = selectedSlice["total investment"];
      } else if (activeButton == "Fund") {
        name = cap(selectedSlice["Asset Name"]);
        value = selectedSlice["Total Investment"];
      } else {
        name = cap(selectedSlice["A.s.set ._Class"]);
        value = selectedSlice["Total Iℂnvest∈d"];
      }
    }

    percentage = totalInvestedInChart > 0 ? (value / totalInvestedInChart) * 100 : 0;

    // Split long names
    const words = name.split(" ");
    const lines = [];
    let currentLine = "";
    
    words.forEach(word => {
      if ((currentLine + " " + word).length > 20) {
        if (currentLine) lines.push(currentLine);
        currentLine = word;
      } else {
        currentLine = currentLine ? currentLine + " " + word : word;
      }
    });
    if (currentLine) lines.push(currentLine);

    // Add name lines
    lines.forEach((line, i) => {
      centerGroup.append("text")
        .attr("text-anchor", "middle")
        .attr("y", -20 + (i * 18))
        .style("font-size", "14px")
        .style("font-weight", "600")
        .style("fill", selectedSlice.isAggregate ? "#8B8B8B" : "var(--pri)")
        .text(line);
    });

    // Add value
    centerGroup.append("text")
      .attr("text-anchor", "middle")
      .attr("y", lines.length * 18)
      .style("font-size", "20px")
      .style("font-weight", "700")
      .style("fill", "var(--founder)")
      .text(formatValue(value));

    // Add percentage
    if (percentage > 0) {
      centerGroup.append("text")
        .attr("text-anchor", "middle")
        .attr("y", lines.length * 18 + 25)
        .style("font-size", "14px")
        .style("font-weight", "500")
        .style("fill", "var(--text-secondary)")
        .text(`${percentage.toFixed(1)}%`);
    }

    // Animate in
    centerGroup.transition()
      .duration(300)
      .style("opacity", 1);
  }

  function handleMouseEnter(event, data) {
    // Scale up on hover
    d3.select(event.currentTarget)
      .transition()
      .duration(200)
      .attr("d", arcHover)
      .style("filter", "brightness(1.1) drop-shadow(0 4px 8px rgba(0,0,0,0.15))");

    // Show tooltip
    let name, value;
    
    if (data.data.isAggregate) {
      name = `Others (${data.data.aggregatedCount} items)`;
      if (activeButton == "Company") {
        value = data.data["total investment"];
      } else if (activeButton == "Fund") {
        value = data.data["Total Investment"];
      } else {
        value = data.data["Total Iℂnvest∈d"];
      }
    } else {
      if (activeButton == "Company") {
        name = cap(data.data["asset"]);
        value = data.data["total investment"];
      } else if (activeButton == "Fund") {
        name = cap(data.data["Asset Name"]);
        value = data.data["Total Investment"];
      } else {
        name = cap(data.data["A.s.set ._Class"]);
        value = data.data["Total Iℂnvest∈d"];
      }
    }

    const percentage = totalInvestedInChart > 0 ? (value / totalInvestedInChart) * 100 : 0;

    let tooltipContent = `
      <div style="font-weight: 600; margin-bottom: 4px;">${name}</div>
      <div style="color: var(--founder); font-weight: 700;">${formatValue(value)}</div>
      <div style="color: var(--text-secondary); font-size: 12px;">${percentage.toFixed(1)}% of total</div>
    `;

    if (data.data.isAggregate && data.data.aggregatedItems) {
      tooltipContent += `<div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid var(--border); font-size: 11px; color: var(--text-secondary);">
        Click to see aggregated items
      </div>`;
    }

    tooltip
      .style("opacity", 1)
      .html(tooltipContent)
      .style("left", (event.pageX + 10) + "px")
      .style("top", (event.pageY - 10) + "px");
  }

  function handleMouseLeave(event, data) {
    // Scale back down
    d3.select(event.currentTarget)
      .transition()
      .duration(200)
      .attr("d", arcPath)
      .style("filter", data.data === selectedSlice ? "brightness(1.1)" : "none");

    // Hide tooltip
    if (tooltip) tooltip.style("opacity", 0);
  }

  function handleSliceClick(event, data) {
    // Update selected slice
    selectedSlice = data.data;
    dispatch("sliceClicked", data.data);
    
    // Update visual selection
    d3.selectAll(".arc path")
      .attr("stroke", (d) => d.data === selectedSlice ? "white" : "none")
      .attr("stroke-width", (d) => d.data === selectedSlice ? "3px" : "0px")
      .style("filter", (d) => d.data === selectedSlice ? "brightness(1.1)" : "none");
    
    updateCenterLabel();
  }

  onMount(() => {
    // Create tooltip
    tooltip = d3.select("body")
      .append("div")
      .attr("class", "chart-tooltip")
      .style("opacity", 0)
      .style("position", "absolute")
      .style("padding", "12px")
      .style("background", "rgba(255, 255, 255, 0.95)")
      .style("border", "1px solid var(--border)")
      .style("border-radius", "8px")
      .style("box-shadow", "0 4px 12px rgba(0,0,0,0.1)")
      .style("pointer-events", "none")
      .style("z-index", "1000")
      .style("font-size", "14px")
      .style("backdrop-filter", "blur(10px)")
      .style("max-width", "200px");

    // Initialize pie generator based on active button
    if (activeButton == "Company") {
      pie = d3.pie()
        .value((d) => {
          const value = d["total investment"];
          return isNaN(value) || value === null || value === undefined ? 0 : Number(value);
        })
        .sort(null)
        .padAngle(0.02);
    } else if (activeButton == "Fund") {
      pie = d3.pie()
        .value((d) => {
          const value = d["Total Investment"];
          return isNaN(value) || value === null || value === undefined ? 0 : Number(value);
        })
        .sort(null)
        .padAngle(0.02);
    } else {
      pie = d3.pie()
        .value((d) => {
          const value = d["Total Iℂnvest∈d"];
          return isNaN(value) || value === null || value === undefined ? 0 : Number(value);
        })
        .sort(null)
        .padAngle(0.02);
    }

    // Initialize arc generators
    arcPath = d3.arc()
      .outerRadius(radius - 20)
      .innerRadius(radius - 80)
      .cornerRadius(4);

    arcHover = d3.arc()
      .outerRadius(radius - 15)
      .innerRadius(radius - 85)
      .cornerRadius(4);

    // Create SVG
    svg = d3.select(".pie-chart")
      .append("svg")
      .attr("width", width)
      .attr("height", height);

    // Add gradient definitions
    const defs = svg.append("defs");
    
    colorPalette.forEach((color, i) => {
      const gradient = defs.append("radialGradient")
        .attr("id", `gradient-${i}`)
        .attr("cx", "30%")
        .attr("cy", "30%");
      
      gradient.append("stop")
        .attr("offset", "0%")
        .attr("stop-color", color)
        .attr("stop-opacity", 1);
      
      gradient.append("stop")
        .attr("offset", "100%")
        .attr("stop-color", d3.color(color).darker(0.5))
        .attr("stop-opacity", 1);
    });

    // Create group for chart
    g = svg.append("g")
      .attr("transform", `translate(${width / 2}, ${height / 2})`);

    // Draw initial chart
    drawChart();

    // Cleanup on unmount
    return () => {
      if (tooltip) tooltip.remove();
    };
  });

  // Redraw chart when data changes
  afterUpdate(() => {
    // Update pie generator based on active button
    if (activeButton == "Company") {
      pie = d3.pie()
        .value((d) => {
          const value = d["total investment"];
          return isNaN(value) || value === null || value === undefined ? 0 : Number(value);
        })
        .sort(null)
        .padAngle(0.02);
    } else if (activeButton == "Fund") {
      pie = d3.pie()
        .value((d) => {
          const value = d["Total Investment"];
          return isNaN(value) || value === null || value === undefined ? 0 : Number(value);
        })
        .sort(null)
        .padAngle(0.02);
    } else {
      pie = d3.pie()
        .value((d) => {
          const value = d["Total Iℂnvest∈d"];
          return isNaN(value) || value === null || value === undefined ? 0 : Number(value);
        })
        .sort(null)
        .padAngle(0.02);
    }
    
    drawChart();
  });
</script>

<div class="pie-chart m-auto" />

<style>
  .pie-chart {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  :global(.arc-path) {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  :global(.center-text text) {
    font-family: 'Inter', sans-serif;
  }
</style>