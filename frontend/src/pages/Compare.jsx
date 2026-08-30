import { Alert, Card, Col, Empty, Row, Select, Space, Statistic, Tag, Typography } from "antd";
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import ForecastChart from "../components/ForecastChart";
import { api, imageUrl } from "../services/api";

export default function Compare() {
  const [params] = useSearchParams();
  const [all, setAll] = useState([]); const [ids, setIds] = useState(() => (params.get("ids") || "").split(",").filter(Boolean).map(Number)); const [designs, setDesigns] = useState([]); const [error, setError] = useState("");
  useEffect(() => { api.listDesigns().then(setAll).catch((reason) => setError(reason.message)); }, []);
  useEffect(() => { if (ids.length === 2) api.compareDesigns(ids).then((result) => setDesigns(result.designs)).catch((reason) => setError(reason.message)); else setDesigns([]); }, [ids]);
  const ready = designs.length === 2 && designs.every((design) => design.forecast);
  return <main className="page"><div className="page-heading"><Typography.Text className="eyebrow">COMPARE</Typography.Text><Typography.Title>方案对比</Typography.Title><Typography.Paragraph>比较设计属性、十周销量曲线和累计预测。</Typography.Paragraph></div><Select mode="multiple" maxCount={2} value={ids} onChange={setIds} placeholder="选择两个方案" style={{ width: "100%", maxWidth: 640, marginBottom: 28 }} options={all.map((design) => ({ value: design.id, label: design.title }))} />{error && <Alert type="error" message={error} />}{designs.length !== 2 ? <Empty description="请选择两个不同方案" /> : <><Row gutter={[20, 20]}>{designs.map((design) => <Col xs={24} md={12} key={design.id}><Card className="compare-card"><div className="compare-head"><img src={imageUrl(design.image_path)} alt={design.title} /><div><Typography.Title level={3}>{design.title}</Typography.Title><Space wrap><Tag>{design.category}</Tag><Tag>{design.color}</Tag><Tag>{design.fabric}</Tag></Space></div></div>{design.forecast ? <Row gutter={12}><Col span={12}><Statistic title="累计预测" value={design.forecast.total_forecast} precision={1} /></Col><Col span={12}><Statistic title="峰值周" value={design.forecast.peak_week} /></Col></Row> : <Alert type="warning" message="该方案尚未生成预测" />}</Card></Col>)}</Row>{ready && <Card className="comparison-chart"><Typography.Title level={3}>十周销量走势</Typography.Title><ForecastChart forecasts={designs.map((design) => design.forecast)} lines={designs.map((design) => design.title)} /></Card>}</>}</main>;
}

