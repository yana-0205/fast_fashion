import { Alert, Button, Empty, Row, Col, Select, Space, Spin, Typography, message } from "antd";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import DesignCard from "../components/DesignCard";
import { api } from "../services/api";

export default function Portfolio() {
  const [designs, setDesigns] = useState([]);
  const [selected, setSelected] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filters, setFilters] = useState({});
  const navigate = useNavigate();

  const load = () => api.listDesigns().then(setDesigns).catch((reason) => setError(reason.message)).finally(() => setLoading(false));
  useEffect(() => { load(); }, []);

  function toggle(id, checked) {
    if (checked && selected.length >= 2) return message.warning("最多选择两个方案");
    setSelected((current) => checked ? [...current, id] : current.filter((value) => value !== id));
  }

  async function remove(id) {
    await api.deleteDesign(id); setSelected((current) => current.filter((value) => value !== id)); load();
  }

  const filtered = designs.filter((design) =>
    (!filters.category || design.category === filters.category) &&
    (!filters.color || design.color === filters.color) &&
    (!filters.fabric || design.fabric === filters.fabric)
  );

  const filterOptions = (field) => [...new Set(designs.map((design) => design[field]))].sort().map((value) => ({ value }));

  return <main className="page"><div className="page-heading"><Typography.Text className="eyebrow">PORTFOLIO</Typography.Text><Typography.Title>方案库</Typography.Title><Typography.Paragraph>保存、筛选并选择两个新品方案进行市场表现对比。</Typography.Paragraph></div>{error && <Alert type="error" message={error} />}<Space wrap className="filter-bar"><Select allowClear placeholder="筛选款式" value={filters.category} onChange={(value) => setFilters((current) => ({ ...current, category: value }))} options={filterOptions("category")} /><Select allowClear placeholder="筛选颜色" value={filters.color} onChange={(value) => setFilters((current) => ({ ...current, color: value }))} options={filterOptions("color")} /><Select allowClear placeholder="筛选材质" value={filters.fabric} onChange={(value) => setFilters((current) => ({ ...current, fabric: value }))} options={filterOptions("fabric")} /><Button onClick={() => setFilters({})}>清除筛选</Button></Space>{loading ? <Spin /> : designs.length === 0 ? <Empty description="还没有方案" /> : filtered.length === 0 ? <Empty description="没有符合条件的方案" /> : <Row gutter={[20, 20]}>{filtered.map((design) => <Col xs={24} sm={12} lg={8} xl={6} key={design.id}><DesignCard design={design} checked={selected.includes(design.id)} onCheck={toggle} onDelete={remove} /></Col>)}</Row>}<div className="floating-action"><Button type="primary" size="large" disabled={selected.length !== 2} onClick={() => navigate(`/compare?ids=${selected.join(",")}`)}>对比已选方案（{selected.length}/2）</Button></div></main>;
}
