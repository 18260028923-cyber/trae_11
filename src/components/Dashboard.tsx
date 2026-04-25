import React, { useState } from 'react'
import {
  Layout,
  Menu,
  theme,
  Card,
  Table,
  Space,
  Button,
  Avatar,
  Dropdown,
  Badge,
  Row,
  Col,
  Statistic,
  Tag,
  Input,
} from 'antd'
import type { MenuProps, TableColumnsType } from 'antd'
import {
  DashboardOutlined,
  ShoppingOutlined,
  UserOutlined,
  SettingOutlined,
  ShopOutlined,
  BellOutlined,
  SearchOutlined,
  DownOutlined,
  ShoppingCartOutlined,
  DollarOutlined,
  TeamOutlined,
  EyeOutlined,
} from '@ant-design/icons'

const { Header, Sider, Content } = Layout

interface DataType {
  key: string
  id: string
  name: string
  category: string
  price: number
  stock: number
  status: string
}

const Dashboard: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false)
  const [selectedKey, setSelectedKey] = useState('dashboard')
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken()

  const menuItems: MenuProps['items'] = [
    {
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: '数据概览',
    },
    {
      key: 'products',
      icon: <ShoppingOutlined />,
      label: '商品管理',
    },
    {
      key: 'orders',
      icon: <ShopOutlined />,
      label: '订单管理',
    },
    {
      key: 'users',
      icon: <UserOutlined />,
      label: '用户管理',
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '系统设置',
    },
  ]

  const userMenuItems: MenuProps['items'] = [
    {
      key: '1',
      label: '个人中心',
    },
    {
      key: '2',
      label: '账户设置',
    },
    {
      type: 'divider',
    },
    {
      key: '3',
      label: '退出登录',
      danger: true,
    },
  ]

  const tableData: DataType[] = [
    {
      key: '1',
      id: 'PRD001',
      name: 'iPhone 15 Pro Max',
      category: '手机数码',
      price: 9999,
      stock: 156,
      status: 'active',
    },
    {
      key: '2',
      id: 'PRD002',
      name: 'MacBook Pro 14寸',
      category: '电脑办公',
      price: 14999,
      stock: 89,
      status: 'active',
    },
    {
      key: '3',
      id: 'PRD003',
      name: 'AirPods Pro 2',
      category: '手机数码',
      price: 1899,
      stock: 0,
      status: 'inactive',
    },
    {
      key: '4',
      id: 'PRD004',
      name: '小米电视 75寸',
      category: '家用电器',
      price: 4999,
      stock: 42,
      status: 'active',
    },
    {
      key: '5',
      id: 'PRD005',
      name: '戴森吸尘器 V15',
      category: '家用电器',
      price: 5490,
      stock: 23,
      status: 'active',
    },
  ]

  const tableColumns: TableColumnsType<DataType> = [
    {
      title: '商品ID',
      dataIndex: 'id',
      key: 'id',
      width: 120,
    },
    {
      title: '商品名称',
      dataIndex: 'name',
      key: 'name',
      width: 200,
    },
    {
      title: '分类',
      dataIndex: 'category',
      key: 'category',
      width: 120,
      render: (text) => <Tag color="blue">{text}</Tag>,
    },
    {
      title: '价格',
      dataIndex: 'price',
      key: 'price',
      width: 120,
      render: (price) => <span style={{ fontWeight: 'bold', color: '#1890ff' }}>¥{price}</span>,
    },
    {
      title: '库存',
      dataIndex: 'stock',
      key: 'stock',
      width: 100,
      render: (stock) => (
        <span style={{ color: stock === 0 ? '#ff4d4f' : '#52c41a' }}>
          {stock === 0 ? '缺货' : stock}
        </span>
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status) => (
        <Tag color={status === 'active' ? 'green' : 'red'}>
          {status === 'active' ? '上架中' : '已下架'}
        </Tag>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: () => (
        <Space size="middle">
          <Button type="link" size="small">
            编辑
          </Button>
          <Button type="link" size="small" danger>
            删除
          </Button>
        </Space>
      ),
    },
  ]

  const handleMenuClick: MenuProps['onClick'] = (e) => {
    setSelectedKey(e.key)
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider
        collapsible
        collapsed={collapsed}
        onCollapse={(value) => setCollapsed(value)}
        theme="dark"
      >
        <div
          style={{
            height: 64,
            margin: 16,
            background: 'rgba(255, 255, 255, 0.2)',
            borderRadius: 8,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontSize: collapsed ? 12 : 18,
            fontWeight: 'bold',
          }}
        >
          {collapsed ? '电商' : '电商后台管理'}
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[selectedKey]}
          items={menuItems}
          onClick={handleMenuClick}
        />
      </Sider>
      <Layout>
        <Header
          style={{
            padding: '0 24px',
            background: colorBgContainer,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            boxShadow: '0 1px 4px rgba(0, 21, 41, 0.08)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', flex: 1, maxWidth: 400 }}>
            <Input
              placeholder="搜索商品、订单、用户..."
              prefix={<SearchOutlined />}
              style={{ borderRadius: borderRadiusLG }}
            />
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
            <Badge count={5} dot>
              <BellOutlined
                style={{
                  fontSize: 20,
                  cursor: 'pointer',
                  color: '#666',
                }}
              />
            </Badge>
            <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  cursor: 'pointer',
                  gap: 8,
                }}
              >
                <Avatar size={32} icon={<UserOutlined />} />
                <span>管理员</span>
                <DownOutlined style={{ fontSize: 12 }} />
              </div>
            </Dropdown>
          </div>
        </Header>
        <Content
          style={{
            margin: '24px 16px',
            padding: 24,
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
          }}
        >
          <div style={{ marginBottom: 24 }}>
            <h2 style={{ fontSize: 20, fontWeight: 600, marginBottom: 8 }}>数据概览</h2>
            <p style={{ color: '#666', fontSize: 14 }}>欢迎回来，查看今日运营数据</p>
          </div>

          <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
            <Col xs={24} sm={12} lg={6}>
              <Card variant="borderless" style={{ borderRadius: borderRadiusLG }}>
                <Statistic
                  title="总销售额"
                  value={1265680}
                  precision={2}
                  valueStyle={{ color: '#3f8600' }}
                  prefix={<DollarOutlined />}
                  suffix="元"
                />
                <div style={{ marginTop: 12, fontSize: 12, color: '#999' }}>
                  较昨日 <span style={{ color: '#52c41a' }}>+12.5%</span>
                </div>
              </Card>
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <Card variant="borderless" style={{ borderRadius: borderRadiusLG }}>
                <Statistic
                  title="订单数量"
                  value={8846}
                  valueStyle={{ color: '#1890ff' }}
                  prefix={<ShoppingCartOutlined />}
                />
                <div style={{ marginTop: 12, fontSize: 12, color: '#999' }}>
                  较昨日 <span style={{ color: '#52c41a' }}>+8.2%</span>
                </div>
              </Card>
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <Card variant="borderless" style={{ borderRadius: borderRadiusLG }}>
                <Statistic
                  title="活跃用户"
                  value={32568}
                  valueStyle={{ color: '#722ed1' }}
                  prefix={<TeamOutlined />}
                />
                <div style={{ marginTop: 12, fontSize: 12, color: '#999' }}>
                  较昨日 <span style={{ color: '#52c41a' }}>+15.3%</span>
                </div>
              </Card>
            </Col>
            <Col xs={24} sm={12} lg={6}>
              <Card variant="borderless" style={{ borderRadius: borderRadiusLG }}>
                <Statistic
                  title="访问量"
                  value={128560}
                  valueStyle={{ color: '#fa8c16' }}
                  prefix={<EyeOutlined />}
                />
                <div style={{ marginTop: 12, fontSize: 12, color: '#999' }}>
                  较昨日 <span style={{ color: '#ff4d4f' }}>-2.4%</span>
                </div>
              </Card>
            </Col>
          </Row>

          <div
            style={{
              marginBottom: 16,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <h3 style={{ fontSize: 16, fontWeight: 600 }}>商品列表</h3>
            <Space>
              <Button>导出数据</Button>
              <Button type="primary">添加商品</Button>
            </Space>
          </div>

          <Card variant="borderless" style={{ borderRadius: borderRadiusLG }}>
            <Table<DataType>
              columns={tableColumns}
              dataSource={tableData}
              pagination={{
                total: 100,
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total) => `共 ${total} 条`,
              }}
            />
          </Card>
        </Content>
      </Layout>
    </Layout>
  )
}

export default Dashboard
