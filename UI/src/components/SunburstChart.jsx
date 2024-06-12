// src/SunburstChart.js
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const SunburstChart = ({ data, width = 500, height = 500 , call_parent_draw_chart }) => {

    const svgRef = useRef();

    useEffect(() => {
        const radius = Math.min(width, height) / 2;
        const partition = d3.partition()
            .size([2 * Math.PI, radius]);

        const root = d3.hierarchy(data)
            .sum(d => d.value)
            .sort((a, b) => b.value - a.value);

        partition(root);
        const color = d3.scaleOrdinal(d3.schemeCategory10);
        const parentColorMap = {};
        root.descendants().forEach(d => {
            if (d.depth === 1) {
                parentColorMap[d.data.name] = color(d.data.name);
            }
        });

        const arc = d3.arc()
            .startAngle(d => d.x0)
            .endAngle(d => d.x1)
            .innerRadius(d => d.y0)
            .outerRadius(d => d.y1);

        const svg = d3.select(svgRef.current)
            .attr('width', width)
            .attr('height', height)
            .append('g')
            .attr('transform', `translate(${width / 2},${height / 2})`);

        svg.selectAll('path')
            .data(root.descendants())
            .enter().append('path')
            .attr('display', d => d.depth ? null : 'none')
            .attr('d', arc)
            .style('stroke', '#fff')
            .style('fill', d => {
                if (d.depth === 1) {
                    return parentColorMap[d.data.name];
                } else {
                    let current = d;
                    while (current.depth > 1) {
                        current = current.parent;
                    }
                    return parentColorMap[current.data.name];
                }
            })
            .on("click", function (event, d) {
                d3.selectAll('path').style('opacity', 1);  // Reset opacity for all paths
                d3.select(this).style('opacity', 0.5); 
                console.log(d.data.name)
                console.log(d.parent.data.name)
                // Extract section name and element type
                if (d.parent.data.name) {
                    // Pass section name and element type to the parent component
                    call_parent_draw_chart(d.parent.data.name, d.data.name)
                }
            });

        svg.selectAll('text')
            .data(root.descendants())
            .enter().append('text')
            .attr('transform', function(d) {
                const x = (d.x0 + d.x1) / 2 * 180 / Math.PI;
                const y = (d.y0 + d.y1) / 2;
                return `rotate(${x - 90})translate(${y},0)rotate(${x < 180 ? 0 : 180})`;
            })
            .attr('dx', '-20')
            .attr('dy', '.35em')
            .text(d => d.data.name)
            .style('font-size', '10px')
            .style('text-anchor', 'middle');

    }, [data, height, width]);

    return (
        <svg ref={svgRef}></svg>
    );
};

export default SunburstChart;
