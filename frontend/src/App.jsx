import { Layout, Menu } from "antd";
import { Link, Route, Routes } from "react-router-dom";
import Compare from "./pages/Compare";
import CreateDesign from "./pages/CreateDesign";
import Dashboard from "./pages/Dashboard";
import DesignDetail from "./pages/DesignDetail";
import Portfolio from "./pages/Portfolio";

const { Header, Content } = Layout;

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
          <Route path="/" element={<Dashboard />} />
          <Route path="/create" element={<CreateDesign />} />
          <Route path="/designs/:id" element={<DesignDetail />} />
          <Route path="/portfolio" element={<Portfolio />} />
          <Route path="/compare" element={<Compare />} />
        </Routes>
      </Content>
    </Layout>
  );
}
