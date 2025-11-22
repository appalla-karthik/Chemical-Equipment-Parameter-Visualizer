import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart, BarElement, CategoryScale, LinearScale } from 'chart.js';

Chart.register(BarElement, CategoryScale, LinearScale);

function ChartPanel({summary}){
  const types = summary.type_distribution;
  const labels = Object.keys(types);
  const values = Object.values(types);

  const data = {
    labels,
    datasets: [{
      label: "Equipment Count by Type",
      data: values
    }]
  };

  return (
    <div style={{width: "400px"}}>
      <Bar data={data}/>
    </div>
  );
}

export default ChartPanel;
