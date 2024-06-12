import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const SunburstSubChart = ({ data,sectionTypeNames ,call_parent_table,width = 500, height = 500  }) => {

    const svgRef = useRef();

    useEffect(() => {
       

        const radius = Math.min(width, height) / 2;
        const partition = d3.partition()
            .size([2 * Math.PI, radius]);

        const root = d3.hierarchy(data)
            .sum(d => d.value)
            .sort((a, b) => b.value - a.value);

        partition(root);
        const customColors = [
            "#e5f392","#58b580","#eef2f3","#b89c93"
        ];
        const color = d3.scaleOrdinal(customColors);

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
            .style('fill', d => color(d.data.name))
            .on("click", function (event, d) {
                d3.selectAll('path').style('opacity', 1);  // Reset opacity for all paths
                d3.select(this).style('opacity', 0.5);  // Highlight the clicked path

                console.log("forwarded data is ", sectionTypeNames);
                console.log(d.data.name);
                if (d.data.name) {
                    call_parent_table(sectionTypeNames.section, sectionTypeNames.type, d.data.name);
                }
            })
            .attr('opacity', 0)
            .transition()
            .duration(1000)
            .attr('opacity', 1)
            .attrTween("d", d => {
                const interpolate = d3.interpolate(d.startAngle, d.endAngle);
                return t => {
                    d.endAngle = interpolate(t);
                    return arc(d);
                };
            });

        // Render text for all nodes, including root
        
        svg.selectAll('text.child-text').remove();

        svg.selectAll('text.child-text')
            .data(root.descendants())
            .enter().append('text')
            .attr('class', 'child-text') // Add a class to distinguish text for child nodes
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

    }, [data, height, width, call_parent_table]);

    return (
        <svg ref={svgRef}></svg>
    );
};

export default SunburstSubChart;
