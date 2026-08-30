import { Button, Card, Checkbox, Space, Tag, Typography } from "antd";
import { Link } from "react-router-dom";
import { imageUrl } from "../services/api";

export default function DesignCard({ design, checked, onCheck, onDelete }) {
  return (
    <Card className="design-card" cover={<img alt={design.title} src={imageUrl(design.image_path)} />}>
      <Typography.Title level={4}>{design.title}</Typography.Title>
      <Space size={[4, 8]} wrap>
        <Tag>{design.category}</Tag><Tag>{design.color}</Tag><Tag>{design.fabric}</Tag><Tag>{design.season}</Tag>
      </Space>
      <div className="card-meta">¥{design.price}</div>
      <div className="card-actions">
        {onCheck && <Checkbox checked={checked} onChange={(event) => onCheck(design.id, event.target.checked)}>加入对比</Checkbox>}
        <Space>
          <Link to={`/designs/${design.id}`}><Button type="link">查看</Button></Link>
          {onDelete && <Button danger type="link" onClick={() => onDelete(design.id)}>删除</Button>}
        </Space>
      </div>
    </Card>
  );
}

