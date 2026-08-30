import { Alert, Button, Card, Col, Form, Input, InputNumber, Row, Select, Skeleton, Space, Statistic, Tag, Typography, message } from "antd";
import { useEffect, useState } from "react";
import ForecastChart from "../components/ForecastChart";
import { api, imageUrl } from "../services/api";

export default function CreateDesign() {
  const [options, setOptions] = useState(null);
  const [design, setDesign] = useState(null);
  const [forecast, setForecast] = useState(null);
  const [insight, setInsight] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api.options().then(setOptions).catch((reason) => setError(reason.message));
  }, []);

  async function submit(values) {
    setLoading(true); setError(""); setForecast(null); setInsight(null);
    try {
      const created = await api.generateDesign(values);
      setDesign(created);
      const prediction = await api.forecastDesign(created.id);
      setForecast(prediction);
      const report = await api.insightDesign(created.id);
      setInsight(report);
      message.success("方案与预测已生成");
    } catch (reason) {
      setError(reason.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="workspace page">
      <div className="page-heading"><Typography.Text className="eyebrow">NEW CONCEPT</Typography.Text><Typography.Title>创建新品方案</Typography.Title><Typography.Paragraph>选择设计属性，系统会匹配相近历史商品并预测未来十周表现。</Typography.Paragraph></div>
      {error && <Alert type="error" showIcon message={error} className="block-gap" />}
      <Row gutter={[24, 24]}>
        <Col xs={24} lg={9}>
          <Card className="panel-card">
            {!options ? <Skeleton active /> : <Form layout="vertical" onFinish={submit} initialValues={{ title: "2026 新品方案", category: options.categories[0], color: options.colors[0], fabric: options.fabrics[0], season: options.seasons[0], price: 399 }}>
              <Form.Item name="title" label="方案名称" rules={[{ required: true }]}><Input /></Form.Item>
              <Row gutter={12}>
                <Col span={12}><Form.Item name="category" label="款式"><Select options={options.categories.map((value) => ({ value }))} /></Form.Item></Col>
                <Col span={12}><Form.Item name="color" label="颜色"><Select options={options.colors.map((value) => ({ value }))} /></Form.Item></Col>
                <Col span={12}><Form.Item name="fabric" label="材质"><Select options={options.fabrics.map((value) => ({ value }))} /></Form.Item></Col>
                <Col span={12}><Form.Item name="season" label="季节"><Select options={options.seasons.map((value) => ({ value }))} /></Form.Item></Col>
              </Row>
              <Form.Item name="price" label="预计售价" rules={[{ required: true }]}><InputNumber min={1} prefix="¥" style={{ width: "100%" }} /></Form.Item>
              <Form.Item name="prompt" label="设计描述"><Input.TextArea rows={3} placeholder="例如：极简廓形、适合通勤" /></Form.Item>
              <Form.Item name="negative_prompt" label="排除元素"><Input placeholder="例如：logo、复杂印花" /></Form.Item>
              <Button block type="primary" htmlType="submit" size="large" loading={loading}>生成并预测</Button>
            </Form>}
          </Card>
        </Col>
        <Col xs={24} lg={15}>
          <Card className="panel-card result-card">
            {!design && !loading && <div className="empty-stage"><Typography.Title level={3}>你的设计结果会显示在这里</Typography.Title><Typography.Paragraph>V1 离线模式使用 Visuelle 2.0 中属性最接近的真实商品图片。</Typography.Paragraph></div>}
            {loading && <Skeleton active paragraph={{ rows: 10 }} />}
            {design && !loading && <>
              <div className="design-result"><img src={imageUrl(design.image_path)} alt={design.title} /><div><Typography.Text className="eyebrow">DATASET MATCH</Typography.Text><Typography.Title level={2}>{design.title}</Typography.Title><Space wrap><Tag>{design.category}</Tag><Tag>{design.color}</Tag><Tag>{design.fabric}</Tag><Tag>{design.season}</Tag></Space><Typography.Paragraph className="source-note">图片来源：{design.image_source}</Typography.Paragraph></div></div>
              {forecast && <section className="insight-section"><Typography.Title level={3}>未来十周销量预测</Typography.Title><Row gutter={16}><Col span={8}><Statistic title="累计预测" value={forecast.total_forecast} precision={1} suffix="件" /></Col><Col span={8}><Statistic title="峰值周" value={forecast.peak_week} prefix="第" suffix="周" /></Col><Col span={8}><Statistic title="风险" value={forecast.risk_level} /></Col></Row><ForecastChart forecasts={[forecast]} lines={[design.title]} /><Typography.Text type="secondary">{forecast.model_version} · 匹配 {forecast.metrics.matched_records} 条记录 · {forecast.metrics.match_level}</Typography.Text></section>}
              {insight && <section className="insight-section"><Typography.Title level={3}>市场洞察</Typography.Title><Alert type="info" showIcon message={insight.summary} /><div className="insight-grid"><Card size="small" title="颜色">{insight.color_analysis}</Card><Card size="small" title="材质">{insight.fabric_analysis}</Card><Card size="small" title="季节">{insight.season_analysis}</Card><Card size="small" title="价格">{insight.price_analysis}</Card></div><Typography.Text type="secondary">解释来源：{insight.source}</Typography.Text></section>}
            </>}
          </Card>
        </Col>
      </Row>
    </main>
  );
}

