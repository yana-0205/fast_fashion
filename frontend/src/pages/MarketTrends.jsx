import { Alert, Card, Col, Row, Skeleton, Statistic, Table, Typography } from "antd";
import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "../services/api";

const columns = [
  { title: "名称", dataIndex: "name" },
  { title: "样本数", dataIndex: "products" },
  { title: "首周均销", dataIndex: "average_sales" },
];

function RankingCard({ title, data, color }) {
  return <Card title={title} className="trend-card"><ResponsiveContainer width="100%" height={260}><BarChart data={data} layout="vertical" margin={{ left: 16, right: 16 }}><CartesianGrid strokeDasharray="4 4" /><XAxis type="number" /><YAxis type="category" dataKey="name" width={100} /><Tooltip /><Bar dataKey="products" fill={color} radius={[0, 5, 5, 0]} /></BarChart></ResponsiveContainer></Card>;
}

export default function MarketTrends() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => { api.marketTrends().then(setData).catch((reason) => setError(reason.message)); }, []);

  return <main className="page"><div className="page-heading"><Typography.Text className="eyebrow">MARKET DATA</Typography.Text><Typography.Title>市场数据趋势</Typography.Title><Typography.Paragraph>在创建新品前查看 Visuelle 2.0 中的商品结构和历史销售节奏。统计结果描述历史数据，不代表因果关系或未来市场保证。</Typography.Paragraph></div>{error && <Alert type="error" message={error} />}{!data ? <Skeleton active paragraph={{ rows: 12 }} /> : <><Row gutter={[16, 16]} className="stats-row"><Col xs={12} md={6}><Card><Statistic title="销售记录" value={data.dataset_rows} /></Card></Col><Col xs={12} md={6}><Card><Statistic title="热门品类" value={data.categories[0]?.name} /></Card></Col><Col xs={12} md={6}><Card><Statistic title="热门颜色" value={data.colors[0]?.name} /></Card></Col><Col xs={12} md={6}><Card><Statistic title="数据来源" value="Visuelle 2.0" /></Card></Col></Row><Card className="trend-card weekly-card"><Typography.Title level={3}>新品发布后十周平均销量</Typography.Title><ResponsiveContainer width="100%" height={320}><LineChart data={data.weekly_average}><CartesianGrid strokeDasharray="4 4" /><XAxis dataKey="week" tickFormatter={(value) => `W${value}`} /><YAxis /><Tooltip /><Line type="monotone" dataKey="sales" stroke="#1f5b45" strokeWidth={3} /></LineChart></ResponsiveContainer></Card><Row gutter={[20, 20]}><Col xs={24} lg={8}><RankingCard title="热门品类" data={data.categories} color="#1f5b45" /></Col><Col xs={24} lg={8}><RankingCard title="热门颜色" data={data.colors} color="#bd7141" /></Col><Col xs={24} lg={8}><RankingCard title="热门材质" data={data.fabrics} color="#657d95" /></Col></Row><Card title="热门品类明细" className="trend-card"><Table rowKey="name" pagination={false} columns={columns} dataSource={data.categories} /></Card><Typography.Text type="secondary">来源：{data.source}</Typography.Text></>}</main>;
}

