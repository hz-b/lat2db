// src/components/LatticeRing.js
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { Tooltip } from 'react-tooltip';
import './LatticeRing.css'; // Import the CSS file

const LatticeRing = ({ elements, onElementClick }) => {
  const svgRef = useRef();

  useEffect(() => {
    if (elements.length > 0) {
      const width = 800;
      const height = 800;
      const radius = Math.min(width, height) / 2 - 50;

      const svg = d3.select(svgRef.current)
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(${width / 2}, ${height / 2})`);

      const angleScale = d3.scaleLinear()
        .domain([0, elements.length])
        .range([0, 2 * Math.PI]);

      const arc = d3.arc()
        .innerRadius(radius - 50)
        .outerRadius(radius);

      svg.selectAll('path')
        .data(elements)
        .enter()
        .append('path')
        .attr('d', (d, i) => {
          const startAngle = angleScale(i);
          const endAngle = angleScale(i + 1);
          return arc({ startAngle, endAngle });
        })
        .attr('fill', (d) => {
          switch (d.type) {
            case 'quadrupole': return 'blue';
            case 'sextupole': return 'red';
            case 'drift': return 'green';
            case 'monitor': return 'orange';
            default: return 'gray';
          }
        })
        .attr('data-tooltip-id', 'element-tooltip')
        .attr('data-tooltip-html', d => `Type: ${d.type}<br>Index: ${d.index}<br>Info: ${d.info}`)
        .on('click', (event, d) => {
          onElementClick(d);
        });

      // Rebuild tooltip
      // The Tooltip component will handle the display
    }
  }, [elements]);

  return (
    <>
      <svg ref={svgRef}></svg>
      <Tooltip id="element-tooltip" html={true} />
    </>
  );
};

export default LatticeRing;
