import { Button, Layout, Menu, Typography } from "antd";
import { Link, Route, Routes } from "react-router-dom";
import Compare from "./pages/Compare";
import CreateDesign from "./pages/CreateDesign";
import DesignDetail from "./pages/DesignDetail";
import Portfolio from "./pages/Portfolio";

const { Header, Content } = Layout;

function Home() {
  return (
    <section className="hero">
      <Typography.Text className="eyebrow">DESIGN WITH EVIDENCE</Typography.Text>
      <Typography.Title>从服装创意到十周需求预测</Typography.Title>
      <Typography.Paragraph>
        创建女装新品方案，用 Visuelle 2.0 多模态数据评估销量潜力，并比较不同设计的市场表现。
      </Typography.Paragraph>
      <Link to="/create"><Button type="primary" size="large">创建新品方案</Button></Link>
    </section>
  );
}

export default function App() {
  return (
    <Layout className="app-shell">
      <Header className="header">
        <Link className="brand" to="/">Fashion Forecast</Link>
        <Menu theme="dark" mode="horizontal" selectable={false} items={[
          { key: "create", label: <Link to="/create">创建方案</Link> },
          { key: "portfolio", label: <Link to="/portfolio">方案库</Link> },
          { key: "compare", label: <Link to="/compare">方案对比</Link> },
        ]} />
      </Header>
      <Content>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/create" element={<CreateDesign />} />
          <Route path="/designs/:id" element={<DesignDetail />} />
          <Route path="/portfolio" element={<Portfolio />} />
          <Route path="/compare" element={<Compare />} />
        </Routes>
      </Content>
    </Layout>
  );
}
