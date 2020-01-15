import { Layout, Breadcrumb, Card, Col, Row, Collapse } from 'antd';
import React from 'react';
import './App.css'

const { Header, Content, Footer } = Layout;
const { Panel } = Collapse;

class App extends React.Component<> {
  render() {
    return (
      <Layout className="layout">
        <Header>
          <div className="logo">
            <span>Dream Factory - Image Semantic Editing</span>
          </div>
        </Header>
        <Content style={{padding: '0 25px'}}>
          <Breadcrumb style={{margin: '16px 0'}}>
          </Breadcrumb>
          {/* select image block*/}
          <Card title="Select a image and have a try!">
            <Row gutter={12}>
              <Col span={4}>
                <Card t hoverable
                      style={{ width: 180 }}
                      bordered={false}
                      cover={<img alt="example" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />}
                >
                  Select this!
                </Card>
              </Col>
              <Col span={4}>
                <Card t hoverable
                      style={{ width: 180 }}
                      bordered={false}
                      cover={<img alt="example" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />}
                >
                  Select this!
                </Card>
              </Col>
              <Col span={4}>
                <Card t hoverable
                      style={{ width: 180 }}
                      bordered={false}
                      cover={<img alt="example" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />}
                >
                  Select this!
                </Card>
              </Col>
              <Col span={4}>
                <Card t hoverable
                      style={{ width: 180 }}
                      bordered={false}
                      cover={<img alt="example" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />}
                >
                  Select this!
                </Card>
              </Col>
              <Col span={4}>
                <Card t hoverable
                      style={{ width: 180 }}
                      bordered={false}
                      cover={<img alt="example" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />}
                >
                  Select this!
                </Card>
              </Col>
              <Col span={4}>
                <Card t hoverable
                      style={{ width: 180 }}
                      bordered={false}
                      cover={<img alt="example" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />}
                >
                  Select this!
                </Card>
              </Col>
            </Row>
          </Card>
          <br />
          {/* Multiple Transform*/}
          <Collapse defaultActiveKey={['1']}>
            <Panel header="Emotion Transform" key="1">

            </Panel>
            <Panel header="Smile Transform" key="2">

            </Panel>
            <Panel header="Age Transform" key="3">

            </Panel>
            <Panel header="Sex Transform" key="4">

            </Panel>
          </Collapse>
        </Content>
        <Footer style={{textAlign: 'center'}}>
          Dream Factory ©2020 Created by Google Winter ML Camp X.Y.Z Team
        </Footer>
      </Layout>
    );
  }
}

export default App;