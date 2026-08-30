import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export default function ForecastChart({ forecasts, lines }) {
  const data = Array.from({ length: 10 }, (_, index) => {
    const row = { week: `W${index + 1}` };
    forecasts.forEach((forecast, forecastIndex) => {
      row[`value${forecastIndex}`] = forecast?.weekly_forecast?.[index] ?? 0;
    });
    return row;
  });

  return (
    <div className="chart-wrap">
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 16, right: 20, bottom: 4, left: 0 }}>
          <CartesianGrid strokeDasharray="4 4" stroke="#dce2dc" />
          <XAxis dataKey="week" />
          <YAxis />
          <Tooltip />
          {forecasts.map((_, index) => (
            <Line key={index} type="monotone" dataKey={`value${index}`} name={lines[index]} stroke={index === 0 ? "#1f5b45" : "#c2713d"} strokeWidth={3} dot={{ r: 3 }} />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

