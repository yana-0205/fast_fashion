import { Button, Card, Col, Empty, Row, Skeleton, Statistic, Typography } from "antd";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import DesignCard from "../components/DesignCard";
import { api, imageUrl } from "../services/api";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => { api.dashboard().then(setData).catch((reason) => setError(reason.message)); }, []);

  return (
    <main>
      <section className="hero dashboard-hero">
        <Typography.Text className="eyebrow">DESIGN WITH EVIDENCE</Typography.Text>
        <Typography.Title>从服装创意到十周需求预测</Typography.Title>
        <Typography.Paragraph>创建女装新品方案，用 Visuelle 2.0 历史数据评估销量潜力，并比较不同设计的市场表现。</Typography.Paragraph>
        <Link to="/create"><Button type="primary" size="large">创建新品方案</Button></Link>
      </section>
      <section className="dashboard-content">
        {!data ? <Skeleton active /> : <>
          <Row gutter={[16, 16]} className="stats-row">
            <Col xs={12} lg={6}><Card><Statistic title="已保存方案" value={data.total_designs} /></Card></Col>
            <Col xs={12} lg={6}><Card><Statistic title="已完成预测" value={data.forecasted_designs} /></Card></Col>
            <Col xs={12} lg={6}><Card><Statistic title="平均十周预测" value={data.average_total_forecast} suffix="件" /></Card></Col>
            <Col xs={12} lg={6}><Card><Statistic title="数据状态" value="Ready" /></Card></Col>
          </Row>
          {data.top_design && <section className="featured-design"><div><Typography.Text className="eyebrow">TOP FORECAST</Typography.Text><Typography.Title level={2}>{data.top_design.title}</Typography.Title><Typography.Paragraph>当前保存方案中十周累计预测最高。</Typography.Paragraph><Link to={`/designs/${data.top_design.id}`}><Button>查看方案</Button></Link></div><img src={imageUrl(data.top_design.image_path)} alt={data.top_design.title} /><Statistic title="累计预测" value={data.top_design.forecast.total_forecast} precision={1} suffix="件" /></section>}
          <div className="section-heading"><Typography.Title level={2}>最近方案</Typography.Title><Link to="/portfolio">查看全部</Link></div>
          {data.recent_designs.length ? <Row gutter={[20, 20]}>{data.recent_designs.map((design) => <Col xs={24} sm={12} lg={6} key={design.id}><DesignCard design={design} /></Col>)}</Row> : <Empty description="还没有保存方案" />}
        </>}
        {error && <Typography.Text type="danger">{error}</Typography.Text>}
      </section>
    </main>
  );
}

