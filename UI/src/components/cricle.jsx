import React from 'react';

function RadialHistogram({ data }) {
  // Define the number of bins and bin size
  const numBins = 12; // You can adjust this based on your preference
  const binSize = 360 / numBins;

  // Initialize an array to hold counts for each bin
  const binCounts = Array(numBins).fill(0);

  // Calculate the counts for each bin
  data.forEach(element => {
    const binIndex = Math.floor(element / binSize);
    binCounts[binIndex]++;
  });

  // Find the maximum count to scale the bars
  const maxCount = Math.max(...binCounts);

  // Define the radius and center of the circle
  const radius = 150;
  const centerX = 200;
  const centerY = 200;

  // Function to calculate the coordinates of a point on the circle
  const getPointCoordinates = (angle, radius, centerX, centerY) => {
    const radians = (angle - 90) * Math.PI / 180;
    const x = centerX + radius * Math.cos(radians);
    const y = centerY + radius * Math.sin(radians);
    return { x, y };
  };

  // Generate paths for each bin segment
  let startAngle = 0;
  const paths = binCounts.map((count, index) => {
    const endAngle = startAngle + binSize;
    const startPoint = getPointCoordinates(startAngle, radius, centerX, centerY);
    const endPoint = getPointCoordinates(endAngle, radius, centerX, centerY);
    const largeArcFlag = count > maxCount / 2 ? 1 : 0;
    const path = `M ${centerX} ${centerY} L ${startPoint.x} ${startPoint.y} A ${radius} ${radius} 0 ${largeArcFlag} 1 ${endPoint.x} ${endPoint.y} Z`;
    startAngle += binSize;
    return <path key={index} d={path} fill="steelblue" />;
  });

  return (
    <svg width={400} height={400}>
      {paths}
    </svg>
  );
}

function App2() {
  // Generate sample data with 1200 elements and random values between 0 and 360
  const data = Array.from({ length: 1200 }, () => Math.floor(Math.random() * 360));

  return (
    <div>
      <h1>Radial Histogram Chart</h1>
      <RadialHistogram data={data} />
    </div>
  );
}

export default App2;
