import { Alert, Card, Col, Row, Space, Spin, Statistic, Tag, Typography } from "antd";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ForecastChart from "../components/ForecastChart";
import { api, imageUrl } from "../services/api";

export default function DesignDetail() {
  const { id } = useParams(); const [design, setDesign] = useState(null); const [error, setError] = useState("");
  useEffect(() => { api.getDesign(id).then(setDesign).catch((reason) => setError(reason.message)); }, [id]);
  if (error) return <main className="page"><Alert type="error" message={error} /></main>;
  if (!design) return <main className="page"><Spin /></main>;
  return <main className="page"><Row gutter={[32, 32]}><Col xs={24} md={9}><img className="detail-image" src={imageUrl(design.image_path)} alt={design.title} /></Col><Col xs={24} md={15}><Typography.Text className="eyebrow">SAVED CONCEPT</Typography.Text><Typography.Title>{design.title}</Typography.Title><Space wrap><Tag>{design.category}</Tag><Tag>{design.color}</Tag><Tag>{design.fabric}</Tag><Tag>{design.season}</Tag></Space><Typography.Title level={3}>¥{design.price}</Typography.Title>{design.forecast && <><Row gutter={16}><Col span={8}><Statistic title="累计预测" value={design.forecast.total_forecast} /></Col><Col span={8}><Statistic title="峰值周" value={design.forecast.peak_week} /></Col><Col span={8}><Statistic title="风险" value={design.forecast.risk_level} /></Col></Row><ForecastChart forecasts={[design.forecast]} lines={[design.title]} /></>}{design.insight && <><Alert className="block-gap" type="info" showIcon message={design.insight.summary} /><div className="insight-grid"><Card size="small" title="颜色">{design.insight.color_analysis}</Card><Card size="small" title="材质">{design.insight.fabric_analysis}</Card><Card size="small" title="季节">{design.insight.season_analysis}</Card><Card size="small" title="价格">{design.insight.price_analysis}</Card></div></>}</Col></Row></main>;
}
